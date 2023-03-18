# booth-23

## Instructions

To play the game, run `python3 main.py` in the main project directory.

## Features

To toggle mask mode, run the game and press `M`. This will show all collidable objects. 

## Map making guidelines

The game automatically processes map info from Tiled so that they interact with the player (collision blocks, spawn point block, etc). To make sure this works correctly, you have to assign Tiled objects certain names. 

Take a look at some of the existing maps in `data/maps` for an example. The important stuff is:

| Tiled object name | Description |
| ----------- | ----------- |
| player_spawn      | Determines where the player will spawn       |
| player_collide   | If player collision, stop player (basic world collision)        |
| death_collide   | If player collision, send player back to spawn point (death)        |
| win_collide   | if player collision, send player to next level        |
| light | Creates a spotlight to illuminate block

### brainstorm

* moving obstacles (level3?, defined paths, player needs to time movement)
* different character per level depending on map (eleven in hospital, etc)
* extras -> eggo waffles, other easter eggs
* jumpscare audio
* eggo -> invincibility

## todo

* ~~Pixel perfect collision with Pygame masks~~
* Add levels (1-2)
* Texture all levels
* Add blocks to change flashlight size as player moves through the world
* Add shader effects

### extras
* secrets
* interact button
* chasing demagorgon
  * faster and faster as the levels progress
  * parallel of candle for demagorgon, glowing red eyes around it
  * teleports closer and closer to the player
