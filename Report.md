# Homework 05 Report

1. What does the `in` operator do? Provide examples of the `in` using strings and lists (or tuples). 
> The in operator in Python is used to check if a value is present in a sequence. It can be used to check for an item in a list or a word in a string.
> E.g
```python 
fruits = ["apple", "banana", "orange"]
   if "apple" in fruits:
    print("Apple is in the list.")

string = "Using in is fun"
    if "in" in string:
    print(string) 

```
2. Taking a moment to research, why would one want to use .casefold() instead of .lower() in python when comparing strings? Please include the reference on where you find the information.
>While they seem to have the same functionality, which is to transform all characters in a string into lower cases, .casefold() is described as more 'agressive', since it also converts language-specific rules and diacritics.
>The .casefold() converts non-ASCII characters to lowercase.
> 
>References: 
> https://www.w3schools.com/python/ref_string_casefold.asp
> https://www.geeksforgeeks.org/difference-between-casefold-and-lower-in-python/

3. For each of the three sequential types you have learned (list, string, tuple) - label as mutable or immutable (refer to the team activity).
>* string - immutable. A string once defined, it cannot be modified. 
E.g.: 
```python
s = "abcde"
s[1] = "z"  # This would raise an error
```

>   * list - muttable. You can change elements inside a list. E.g.
>  
```python
s = [1, 2, 3, 4, 5]
s[1] = 3 '''This substitutes the second element in the list with a 3'''
```
>* tuple - immutable. While it is not possible to modify a tuple, it is possible for example to 
create new ones from an existing tuple.
E.g:

4. Explain mutability and immutability in your own words.
> Mutability is when the original value can be modified in the same variable. One example is 
the list in the above question. Immutable is when an original value cannot be modified, if there is a neeed
to have a modified version, a new object needs to be created using the original one.

5. Given the following code:

    ```python
    def mystery_function(x):
        x = 100

    x = 1
    print(x)
    mystery_function(x)
    print(x)
    ```

* What is the output of the code above?
>1
> 
>1
  
* Explain why the output is what it is.
>When the function is called with x as argument, the function is working with the original
> x variable as reference. In the code above, x is being created as a new variable inside the function myster_function(), with local scope.
> To modify the value of the original variable, we would need to use the global keyword inside the function, to 
> define that we are referring to the global variable.

6. Given the following code:

    ```python
    def mystery_function(x):
        x[0] = 100

    x = [1, 2, 3]
    print(x)
    mystery_function(x)
    print(x)
    ```
* What is the output of the code above? 
>[1, 2, 3]
> 
>[100, 2, 3]
>
* Explain why the output is what it is.
>Lists are mutable data structures, so when you are working with them, the changes made within
> a function that is working with that variable can change it. That is why the output is a list
> with it's first element changed after calling the function in main.

7. Would happen if `x` was a tuple? What is generated when you try to run the code above with a tuple?
>If 'x' was a tuple, an error would be thrown, since tuples are immutable subjects.  


>    TypeError: 'tuple' object does not support item assignment




8. Given the following code:

    ```python
    def mystery_function(x):
        x[1][0] = 100

    x = (3, [1, 2, 3], [4, 5, 6])
    print(x)
    mystery_function(x)
    print(x)
    ```

* What is the output of the code above?
>(3, [1, 2, 3], [4, 5, 6])
>
>(3, [100, 2, 3], [4, 5, 6])


## Deeper Thinking

We talked a lot about immutable and mutable. Why would this matter? 
Take a moment to describe in your own words why computers would care. 
Pay particular attention to how computers store data in memory, and how 
making something immutable may help with that storage.

>From a development perspective, knowing which objects are mutable and immutable 
will be essential - as we would not want to write code that tries to change immutable 
objects. 
> 
>For computers, regarding memory management, mutable objects are easier to manage, since
they can be reused, therefore they can be cached, optimized for faster access. 
> 
> Immutable objects can be shared  between multiple parts of a program. Since they can't be modified, there's no 
> risk of one part of the program changing the object and affecting other parts. 

>Resources: https://www.learningjournal.guru/article/scala/functional-programming/immutability-in-functional-programming/
> https://realpython.com/python-mutable-vs-immutable-types/
> https://medium.com/@farihatulmaria/how-does-python-manage-memory-explain-the-difference-between-mutable-and-immutable-objects-faa0bfe3b1e7#:~:text=Immutable%20objects%20are%20easier%20to,objects%2C%20leading%20to%20potential%20fragmentation.