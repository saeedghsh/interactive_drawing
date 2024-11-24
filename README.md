# Drawing with Python

### Inspirations for drawings
* [Algorithmic Mathematical Art By Xah Lee](http://xahlee.info/math/algorithmic_math_art.html)
* [Polyhedra by Robert Webb](https://www.software3d.com/FedSquare.php)
* [Interesting visualization by saharan](https://oimo.io/works)

## Laundry List
* [x] [refactor] clean up Game/Grid classes
* [x] [performance] start with profiling the code as is
    ```bash
    python -m cProfile -o profile_output.prof interactive_grid.py
    snakeviz profile_output.prof
    ```
* [x] [performance] use numpy; vectorize, random number generation
* [ ] [performance] use `lru_cache` for the functions that can be cached
* [ ] [performance] use `from numba import njit`
* [ ] [variant] Instead of slider, use a continuous and gradual change of angle
* [ ] [variant] Instead of mouse curser, use a smooth-random moving point
* [ ] [variant] add color

## License
Distributed with a GNU GENERAL PUBLIC LICENSE; see [LICENSE](https://github.com/saeedghsh/interactive_drawing/blob/master/LICENSE).
```
Copyright (C) Saeed Gholami Shahbandi
```
NOTE: Portions of this code/project were developed with the assistance of ChatGPT, a product of OpenAI.  
