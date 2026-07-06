# TSP Sample Datasets

Sample CSV files for testing the TSP Solver. Each demonstrates different patterns and problem difficulties.

## Files

### sample-cities.csv (100 cities) ⭐ Default
- **Cities**: 100
- **Pattern**: Random distribution
- **Difficulty**: Medium
- **Best Known Distance**: ~1,710 units
- **Optimal**: Unknown (NP-hard)
- **Use Case**: Standard testing, realistic scenario
- **Solver Time**: 2-6 seconds

### sample-small.csv (10 cities)
- **Cities**: 10
- **Pattern**: Simple rectangular layout
- **Difficulty**: Easy (trivial optimal is clear)
- **Best Known**: ~50 units (square perimeter)
- **Optimal**: Easy to verify
- **Use Case**: Quick testing, demonstration, learning
- **Solver Time**: <100ms
- **Example**: Perfect for understanding how the solver works

### sample-medium.csv (50 cities)
- **Cities**: 50
- **Pattern**: Clustered in 10 groups of 5
- **Difficulty**: Medium
- **Best Known**: ~250-300 units
- **Optimal**: Unknown
- **Use Case**: Balanced complexity, real-world clusters
- **Solver Time**: 1-3 seconds
- **Example**: Mimics geographic clusters (cities grouped by region)

### sample-circle.csv (40 cities)
- **Cities**: 40
- **Pattern**: 2 concentric circles (20 outer, 20 inner)
- **Difficulty**: Medium (optimal is almost obvious)
- **Best Known**: ~400 units (outer + inner circles)
- **Optimal**: ~398 units (two perfect circles)
- **Use Case**: Benchmark against theory, visualization testing
- **Solver Time**: 1-2 seconds
- **Example**: Excellent for testing visualization - shows clear circular pattern

### sample-grid.csv (36 cities)
- **Cities**: 36
- **Pattern**: 6×6 perfect grid
- **Difficulty**: Easy-Medium (structured)
- **Best Known**: 110 units (row-by-row Hamiltonian path)
- **Optimal**: 110 units (proven by pattern)
- **Use Case**: Testing on structured data, algorithm benchmark
- **Solver Time**: 500ms - 2 seconds
- **Example**: Perfect for grid-like problems (scheduling, map grids, etc.)

---

## How to Use

1. **In the TSP Solver UI**:
   - Click "📤 Upload CSV"
   - Select any of these sample files
   - Click "▶️ Run Solver"

2. **Format Requirements**:
   - Must have header: `X_Final,Y_Final`
   - Two columns: X coordinate, Y coordinate
   - Numbers separated by comma
   - 3-1000 cities supported

3. **Expected Results**:
   ```
   Random (100 cities):  ~1,710 units (85% better than random ~10,300)
   Small (10 cities):    ~50 units    (optimal path around square)
   Medium (50 cities):   ~250 units   (cluster-to-cluster path)
   Circle (40 cities):   ~400 units   (trace both circles)
   Grid (36 cities):     ~110 units   (row-by-row sweep)
   ```

---

## Difficulty Levels

| Level | Example | Cities | Time | Optimal Known? |
|-------|---------|--------|------|----------------|
| **Easy** | Small, Grid | 10-36 | <1s | Yes |
| **Medium** | Circle, Medium | 40-50 | 1-3s | Partial |
| **Hard** | Cities (random) | 100+ | 2-6s | No |
| **Very Hard** | 500+ random | 500+ | 10-30s | No |

---

## Understanding Results

### Quality Metrics
- **Random Baseline**: Shuffled random path
- **Your Solution**: Optimized path from solver
- **Improvement %**: `(Random - Optimized) / Random × 100`
- **Typical Quality**: 80-85% better than random

### Segment Analysis
- **Short Segments** (green): <20 units, well-connected cities
- **Long Segments** (red): >50 units, sparse regions
- **Ideal Route**: Minimal long segments, balanced distribution

### Convergence
- **Initial (NN)**: First heuristic solution
- **2-Opt**: Removes crossing edges (~10% improvement)
- **Or-Opt**: Fine-tunes segments (~2-5% improvement)
- **Plateau**: When 2-Opt can't find more improvements

---

## Tips for Best Results

1. **For Learning**: Start with `sample-small.csv` (10 cities)
2. **For Demonstration**: Use `sample-circle.csv` (clear pattern)
3. **For Realistic**: Use `sample-cities.csv` (100 cities, random)
4. **For Benchmarking**: Use `sample-grid.csv` (structured, deterministic)

---

## Creating Your Own

CSV Format:
```
X_Final,Y_Final
10.5,20.3
12.1,19.8
11.2,21.5
...
```

Tips:
- Use realistic coordinate ranges (e.g., latitude/longitude: -180 to 180)
- Include 3-1000 cities for best results
- Clustered data (geographic) often has better solutions
- Random data is harder (closer to NP-complete)

---

*Dataset Info: Created for TSP Solver testing at intellibloom.web.app*
