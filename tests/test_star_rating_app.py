
import unittest
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import re
import io


import star_rating_app # type: ignore



# lambda function to make feedback messages easier to read
common_msg = lambda msg, expected, actual: f"{msg}\nExpected: {expected}\nActual: {actual}"

# quick 'lambda' function to clean up spaces in strings
clean_spaces = lambda s: re.sub(r'\s+', '', s)

MOVIES_DEFAULT = [
    ("Princess Bride", 10),
    ("Jurassic Shark", 1),
    ("V", 5),
    ("It's A Wonderful Life", 2),
    ("Corpse Bride", 5),
    ("The Princess Diaries", 3),
    ("The Matrix", 4),
    ("The Matrix Reloaded", 3),
    ("The Matrix Revolutions", 2),
    ("The Matrix 4", 4)
]




class TestStarRatingApp(unittest.TestCase):

    def _helper_clean_title(self, inpt, expected) -> None:
        """Helper method to make repeated tests easier"""
        actual = star_rating_app.clean_title(inpt)
        self.assertEqual(actual, expected, 
            common_msg(f"Title did not clean properly with input {inpt}.", expected, actual))

    def _helper_add_movie(self, movie_str, expected) -> None:
        """Helper method to make repeated tests easier""" 
        actual = star_rating_app.convert_str_movie_tuple(movie_str)
        if type(actual) != tuple:
            self.fail(f"Return type {actual} is not a tuple. It is type {type(actual)}.")  
        self.assertEqual(actual, expected, 
            common_msg(f"Title did not clean properly with input {movie_str}.", str(expected), str(actual)))


    def _helper_convert_rating(self, val, expected) -> None:
        """Helper method to make repeated tests easier"""
        actual = star_rating_app.convert_rating(val)
        expected = "*" * expected
        self.assertEqual(actual, expected, 
            common_msg(f"Rating did not convert properly with input {val}.", expected, actual))

    def test_clean_title(self) -> None:
        """Sends various titles to clean titles, to make sure they are cleaned properly. Simple cases."""
        self._helper_clean_title("v", "V")
        self._helper_clean_title("princess bride", "Princess Bride")
        self._helper_clean_title("    Princess Bride", "Princess Bride")
    
    def test_add_movie(self) -> None:
        """Testing add movie with easy input strings, checking to make sure a tuple returns."""
        self._helper_add_movie("v,5", ('V', 5))
        self._helper_add_movie("Princess Bride,100", ("Princess Bride", 100))
        self._helper_add_movie("Jurassic Shark,1", ("Jurassic Shark", 1))

    def test_convert_rating(self) -> None:
        """Testing convert rating with standard range ratings."""
        self._helper_convert_rating(5, 5)
        self._helper_convert_rating(1, 1)
        self._helper_convert_rating(3, 3)

    def test_clean_title_hard(self) -> None:
        """Sends various titles to clean titles, to make sure they are cleaned properly. Hard cases."""
        self._helper_clean_title("It's a wonderful life", "It's A Wonderful Life")
        self._helper_clean_title("    PrinCesS bRide        \t\n", "Princess Bride")

    def test_add_movie_hard(self) -> None:
        """Testing add movie with HARD input strings. (could even be negative numbers)"""
        self._helper_add_movie("Princess Bride,100", ("Princess Bride", 100))
        self._helper_add_movie("Jurassic Shark,-10", ("Jurassic Shark", -10))
        self._helper_add_movie("It's A wondERful life    ,   -10  ", ("It's A Wonderful Life", -10))

    def test_convert_rating_hard(self) -> None:
        """Testing convert rating with out of bounds ranges."""
        self._helper_convert_rating(100, 5)
        self._helper_convert_rating(-100, 1)
        self._helper_convert_rating(0, 1)
        actual = star_rating_app.convert_rating(10, min_stars=3, max_stars=6)
        expected = 6 * "*"
        self.assertEqual(actual, expected,
            common_msg("Rating did not convert properly with input {10, min_stars = 3, max_stars = 6}.", expected, actual))

    def test_check_filter_no_filter(self) -> None:
        """Tests the check_filter function with no filter."""
        for movie in MOVIES_DEFAULT:
             self.assertTrue(star_rating_app.check_filter(movie, ''), 
                common_msg(f"Filter did not work properly with input {movie}.", True, False)) 

    def test_check_filter_movie_title_filter(self) -> None:
        """Tests the check_filter function with a movie title filter."""
        for movie in [x for x in MOVIES_DEFAULT if 'princess' in x[0].casefold()] :
            self.assertTrue(star_rating_app.check_filter(movie, 'princess'), 
                common_msg(f"Filter did not work properly with input {movie}.", True, False)) 
        for movie in [x for x in MOVIES_DEFAULT if 'jurassic' not in x[0].casefold()] :
            self.assertFalse(star_rating_app.check_filter(movie, 'jurassic'), 
                common_msg(f"Filter did not work properly with input {movie}.", False, True))   
    
    def test_check_filter_movie_rating_filter(self) -> None:
        """Tests the check_filter function with a movie rating filter."""
        for movie in [x for x in MOVIES_DEFAULT if x[1] >= 4] :
            self.assertTrue(star_rating_app.check_filter(movie, '>= 4'), 
                common_msg(f"Filter did not work properly with input {movie}.", True, False)) 
        for movie in [x for x in MOVIES_DEFAULT if x[1] < 4] :
            self.assertTrue(star_rating_app.check_filter(movie, '< 4'), 
                common_msg(f"Filter did not work properly with input {movie}.", True, False)) 
        for movie in [x for x in MOVIES_DEFAULT if x[1] == 4] :
            self.assertTrue(star_rating_app.check_filter(movie, '= 4'), 
                common_msg(f"Filter did not work properly with input {movie}.", True, False)) 
        for movie in [x for x in MOVIES_DEFAULT if x[1] != 4] :
            self.assertTrue(star_rating_app.check_filter(movie, '!= 4'), 
                common_msg(f"Filter did not work properly with input {movie}.", True, False)) 

    def test_print_list(self) -> None:
        """Tests the print_list function with a list of movies to check for valid printing."""
        expected = """
*****  Princess Bride
*      Jurassic Shark
*****  V
**     It's A Wonderful Life
*****  Corpse Bride
***    The Princess Diaries
****   The Matrix
***    The Matrix Reloaded
**     The Matrix Revolutions
****   The Matrix 4""".strip()
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            star_rating_app.print_movies(MOVIES_DEFAULT)  
            actual = mock_stdout.getvalue().strip()
            self.assertTrue(clean_spaces(expected) in clean_spaces(actual), 
                msg=common_msg("Printed list did not match expected output (order matters).", expected="\n"+expected, 
                               actual="\n"+actual))    
        
    def test_print_list_filtered(self) -> None:
        """Tests the print_list function with a list of movies to check for valid printing and a filter."""
        expected = """
*****  Princess Bride
***    The Princess Diaries""".strip()
        filtered = [x for x in MOVIES_DEFAULT if 'princess' in x[0].casefold()]
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            star_rating_app.print_movies(filtered)  
            actual = mock_stdout.getvalue().strip()
            self.assertTrue(clean_spaces(expected) in clean_spaces(actual), 
                msg=common_msg("Printed list did not match expected output (order matters).", expected="\n"+expected, 
                               actual="\n"+actual))     

    @patch('builtins.input', side_effect=['exit'])
    def test_run_two(self, mock_input) -> None:
        """Tests a basic run but simply exists"""
        expected = "Welcome to the movie tracker!\nEnter a movie and rating to add it to the list.\n" + \
                   "Thanks for using the movie tracker!\n" + \
                   "Sadly, movies will not be saved, as we still need to learn how to write to files."
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            star_rating_app.run()
            self.assertEqual(mock_stdout.getvalue().strip(), 
                expected.strip(), 
                msg=common_msg("Did not match expected output.", expected= "\n" + expected,
                               actual = "\n" + mock_stdout.getvalue()))


    @patch('builtins.input', side_effect=['add Princess Bride,100', 'add Corpse Bride, 5', 'list', 'exit'])
    def test_run(self, mock_input) -> None:
        """Tests a basic run by adding two movies, printing them, and then exiting"""
        expected = "Welcome to the movie tracker!\nEnter a movie and rating to add it to the list.\n" + \
                   "*****  Princess Bride\n*****  Corpse Bride\n" + \
                   "Thanks for using the movie tracker!\n" + \
                   "Sadly, movies will not be saved, as we still need to learn how to write to files."
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            star_rating_app.run()
            self.assertEqual(mock_stdout.getvalue().strip(), 
                expected.strip(), 
                msg=common_msg("Printed did not match expected output.", expected= "\n" + expected,
                               actual = "\n" + mock_stdout.getvalue()))
    


if __name__ == '__main__':
    unittest.main()
