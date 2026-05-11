> **Warning!** I am not an experienced datapack developer. I do, however, know like 8 general purpose programming languages and most Minecraft commands, so I randomly decided to make a new Python file, open [minecraft.wiki](https://minecraft.wiki), and convert some video to holograms. Beware of unoptimized and **bad** code!

<div align="center">
    <h1>mcvideoholo</h1>
</div>

Hey guys! It's me, Floor Mann, back at it with yet another **mildly** useful project! This datapack generator for **Minecraft: Java** version 26.1.2 uses Python to convert an MP4 file to holograms, which are armor stands for the reason of possible backwards compatibility in the future.

These armor stands are cool. Their names have full support for JSON text components, therefore they support RGB pixels using the square character!

While I don't have full video playback yet (accurate FPS will probably be a burden, or not?) you can **still** play the video with a repeater chain of command blocks!

## How to Run

Run [main.py](main.py) with Python, then run [datapack.py](datapack.py). [main.py](main.py) outputs `.mcfunction` files to [output/](output/), and [datapack.py](datapack.py) generates a datapack with that!

Load the datapack into your world. Join the world, and run these commands in-order:
```mcfunction
/function mcvideoholo:setup
/function mcvideoholo:frame_0000
```

Walk away from where you were and look. Right in front of you should be a grid of RGB pixels! Change the number in that last command for a different frame of the video, and you should be good to go.

Once you're done with that pixel grid, you can run this command to get rid of it:
```mcfunction
/function mcvideoholo:cleanup
```

> **Note:** Only one pixel grid is supported at a time!
