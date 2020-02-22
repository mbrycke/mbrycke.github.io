
## OpenAI

To install openai on linux (tested on Ubuntu 18) you should first create an environment. If you are using conda:

```ssh
conda create --name name_of_openai_environment
```

Install OpenAI gym with pip:

```ssh
pip install gym
```

There are a few openai enviroments you can run rightaway without additional packeges. E.g. CarPole-v1.
We are going to experiment with LunarLander-v2 which needs Box2D:

```ssh
pip install Box2D
```

Similarly there are other packages needed for e.g. the Robotics environment. https://gym.openai.com/envs/#robotics

