
## Benchmark Generation
The following instructions have been tested on macOS Sequoia 15.3


1. Clone [`pddl-generators` repository](https://github.com/AI-Planning/pddl-generators) into `util` directory:
```
 cd util && git clone https://github.com/AI-Planning/pddl-generators
```

2. Build all PDDL generators:
```
cd pddl-generators && ./build_all
```

3. Move the `matchingbw` generator out of `blocksworld` for the trajectory 
generator to work correctly
```
mv blocksworld/matching matchingbw
cp -r blocksworld/bwstates.1 ./
```

4. Install `requirements.txt`
```
cd ../../ && pip install -r requirements.txt
```

5. Generate trajectories:
```
cd util && python gen_trajs_learning.py
```


> [!NOTE]
> **Reproducibility**: the benchmark generation process and evaluation results 
> are reproducible with fixed computational resources.




### Domain selection
The adopted domains are the ones from all past IPC learning tracks:
1. [IPC 2008 Learning Track](https://ipc08.icaps-conference.org/learning/): `goldminer`, `matchingbw`, `npuzzle`, 
`parking` and `sokoban`
> [!WARNING]
> `thoughtful`: has not been considered since there is no problem generator neither in the IPC 
> resources nor in [`pddl-generators` repository](https://github.com/AI-Planning/pddl-generators).

2. [IPC 2011 Learning Track](https://icaps11.icaps-conference.org/proceedings/pal/fawcett-et-al.pdf): `barman`, 
`blocksworld`, `depots`, `gripper`, `parking`, `rovers`, `satellite`, `spanner` and `tpp`.
3. [IPC 2014 Learning Track](https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/2571): `elevators`,
`floortile`, `nomystery`, `parking`, `spanner` and `transport`.
4. [IPC 2023 Learning Track](https://github.com/ipc2023-learning/benchmarks): `blocksworld`,
`childsnack`, `ferry`, `floortile`, `miconic`, `rovers`, `satellite`, `sokoban`,
`spanner` and `transport`.
> [!WARNING]
> `childsnack`: for compatibility with the problems generator, we adopted the original domain 
> version without negative preconditions.

Therefore the following set of 20 classical planning domains:


<table class="dataframe">
  <thead>
<tr style="text-align: left;">
  <th rowspan="2">Domain name</th>
  <th rowspan="2">Operators</th>
  <th rowspan="2">Predicates</th>
  <th rowspan="2">Types</th>
  <th colspan="2">Max arity</th>
  <th colspan="2">Min arity</th>
</tr>
<tr>
  <th>Operators</th>
  <th>Predicates</th>
  <th>Operators</th>
  <th>Predicates</th>
</tr>
  </thead>
  <tbody>
    <tr>
      <td>barman</td>
      <td>12</td>
      <td>15</td>
      <td>9</td>
      <td>6</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <td>blocksworld</td>
      <td>4</td>
      <td>5</td>
      <td>1</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <td>childsnack</td>
      <td>6</td>
      <td>13</td>
      <td>6</td>
      <td>4</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <td>depots</td>
      <td>5</td>
      <td>6</td>
      <td>9</td>
      <td>4</td>
      <td>2</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <td>elevators</td>
      <td>6</td>
      <td>8</td>
      <td>5</td>
      <td>5</td>
      <td>2</td>
      <td>3</td>
      <td>2</td>
    </tr>
    <tr>
      <td>ferry</td>
      <td>3</td>
      <td>5</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>0</td>
    </tr>
    <tr>
      <td>floortile</td>
      <td>7</td>
      <td>10</td>
      <td>3</td>
      <td>4</td>
      <td>2</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <td>goldminer</td>
      <td>7</td>
      <td>12</td>
      <td>1</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <td>grippers</td>
      <td>3</td>
      <td>4</td>
      <td>4</td>
      <td>4</td>
      <td>3</td>
      <td>3</td>
      <td>2</td>
    </tr>
    <tr>
      <td>matchingbw</td>
      <td>10</td>
      <td>10</td>
      <td>2</td>
      <td>3</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <td>miconic</td>
      <td>4</td>
      <td>6</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <td>nomystery</td>
      <td>3</td>
      <td>6</td>
      <td>5</td>
      <td>6</td>
      <td>3</td>
      <td>3</td>
      <td>2</td>
    </tr>
    <tr>
      <td>npuzzle</td>
      <td>1</td>
      <td>3</td>
      <td>2</td>
      <td>3</td>
      <td>2</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <td>parking</td>
      <td>4</td>
      <td>5</td>
      <td>2</td>
      <td>3</td>
      <td>2</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <td>rovers</td>
      <td>9</td>
      <td>25</td>
      <td>7</td>
      <td>6</td>
      <td>3</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <td>satellite</td>
      <td>5</td>
      <td>8</td>
      <td>4</td>
      <td>4</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <td>sokoban</td>
      <td>2</td>
      <td>4</td>
      <td>3</td>
      <td>5</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <td>spanner</td>
      <td>3</td>
      <td>6</td>
      <td>5</td>
      <td>4</td>
      <td>2</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <td>tpp</td>
      <td>4</td>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>3</td>
      <td>3</td>
      <td>2</td>
    </tr>
    <tr>
      <td>transport</td>
      <td>3</td>
      <td>5</td>
      <td>6</td>
      <td>5</td>
      <td>2</td>
      <td>3</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
