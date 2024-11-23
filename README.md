# Drawing with Python

### Inspirations for drawings
* [Algorithmic Mathematical Art By Xah Lee](http://xahlee.info/math/algorithmic_math_art.html)
* [Polyhedra by Robert Webb](https://www.software3d.com/FedSquare.php)
* [Interesting visualization by saharan](https://oimo.io/works)


## Laundry List
* [x] refactor, clean up Game/Grid names
* [x] start with profiling the code as is
    ```bash
    python -m cProfile -o profile_output.prof interactive_grid.py
    snakeviz profile_output.prof
    ```
* [x] use numpy; vectorize, random number generation
* [ ] use `lru_cache` for the functions that can be cached
* [ ] use `from numba import njit`


## License
Distributed with a GNU GENERAL PUBLIC LICENSE; see [LICENSE](https://github.com/saeedghsh/interactive_drawing/blob/master/LICENSE).
```
Copyright (C) Saeed Gholami Shahbandi
```
NOTE: Portions of this code/project were developed with the assistance of ChatGPT, a product of OpenAI.  
