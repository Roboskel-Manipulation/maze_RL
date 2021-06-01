# maze_RL

### Description
A human-agent collaborative game in a [virtual environment](https://github.com/ThanasisTs/maze_RL/tree/main/maze3D) based on the work of Shafti et al. (2020) [1]. Collaborative Learning is achieved through deep Reinforcement Learning (DRL). The Soft-Actor Critic (SAC) algorithm is used [2] with modifications for discrete action space [3].


### Installation
* Run `source install_dependencies/install.sh`. A python virtual environment will be created and the necessary libraries will be installed. Furthermore, the directory of the repo will be added to the `PYTHONPATH` environmental variable.

### Run
* Run `python game/maze3d_human_only_test.py game/config/config_human_test.yaml` for human-only game.
* Run `python game/sac_maze3d_train.py game/config/<config_sac> <participant_name>` for human-agent game.
  * Notes before training: 
     * Set the <participant_name> to the name of the participant.
     * The program will create a `/tmp` and a `/plot` folder (if they do not exist). The `/tmp` folder contains CSV files with information of the game. The `/plot` folder contains figures for tha game.
     * The program will automatically create an identification number after your name on each folder name created

### Configuration
* In the game/config folder several YAML files exist for the configuration of the game. The main parameters are listed below.
    * `game/discrete`: True if the keyboard input is discrete (False for continuous). Details regarding the discrete and continuous human input mode can be found [here](https://github.com/ThanasisTs/maze_RL/tree/main/game)
    * `SAC/reward_function`: Type of reward function. Details about the predefined reward funtions and how to define a new one can be found [here](https://github.com/ThanasisTs/maze_RL/tree/main/game).
    * `Experiment/loop`: Choose how the game will be terminated; either when a number of episodes or a number of interactions is completed.
    * `SAC/discrete`: Discrete or normal SAC (Currently only the discrete SAC is compatible with the game)
  
### Play
![Game](https://github.com/ThanasisTs/maze_RL/blob/main/pictures/maze_tilt.png)

* `Human only`: Use Left and Right arrows to control the tilt of the tray around its y-axis and use Up and Down arrows to control the tile of the tray around its x-axis as shown in the previous picture
* `Human-Agent`: Use Left and Right arrows to control the tilt of the tray around its y-axis
* Press once the spacekey to pause and a second time to resume
* Press q to exit the experiment.

### References
[1] Shafti, Ali, et al. "Real-world human-robot collaborative reinforcement learning." arXiv preprint arXiv:2003.01156 (2020).

[2] https://github.com/kengz/SLM-Lab

[3] Christodoulou, Petros. "Soft actor-critic for discrete action settings." arXiv preprint arXiv:1910.07207 (2019).
