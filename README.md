# Space2Sound

## Inspiration
This project stands at the intersection of art and science, where ancient human fascination with the cosmos meets cutting-edge technology to offer a sensory experience. By leveraging sonification, it helps redefine our relationship with space, making astronomy more than just a subject of visual observation. Historically, humans have always looked to the stars for inspiration, from the arts and beliefs in the religions of early ancient civilizations such as the Babylonians, Egyptians, and Greeks to the precision in the astronomical scale in science. This project echoes this timeless impulse of humans to space but reframes it in a more modern and technological setting, providing the public with an additional dimension of the universe.

## Project Details

### Parameters for Sonification
- **Distance(Parsecs)**: maps note timing. Stars farther away are represented as later notes in the sequence
- **Magnitude(Apparent Brightness)**: maps to pitch. Brighter stars mean higher pitches and dimmer stars mean lower pitch
- **Color Index(Ci)**: map to velocity (volume). Lower value which means bluer/hotter stars maps to lower volume and vice versa

### Data Visualization
Because of the sheer scale of the datasets, we truncated the dataset for simplicity

- **Raw Data** (90% stars discovered): Represents the completeness of the ATHYG Database in terms of known stars (approxiamtely 990 millions of stars)
![Alt Text](/plots/hyg_raw.png)

- **Sonified Data** (0.3% stars sonified): Represents the the subset of stars from the ATHYG database has been sampled for this project (about 3 million stars)
![Alt Text](/plots/hyg.png)


## Data Source

This project uses the **ATHYG Database**, a star catalog that combines data from multiple sources, including Hipparcos, Tycho-2, and Gaia, to provide comprehensive information about stars.

- **Name**: ATHYG Database  
- **Author(s)**: Astronexus  
- **License**: [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)  
- **GitHub Repository**: [https://github.com/astronexus/ATHYG-Database](https://github.com/astronexus/ATHYG-Database)  
- **Description**: The ATHYG Database is an extended version of the HYG database, integrating additional data sources for improved star catalog accuracy.

If you use this project or its datasets, please attribute the ATHYG Database appropriately. Suggested citation:

> Astronexus. (2023). ATHYG Database. Retrieved from https://github.com/astronexus/ATHYG-Database. Licensed under CC BY 4.0.
