from protomask import anim_runner
import sys

print("pico booted")

print("programs: anim_runner, quit")
print(f"program to run?")

inpt = input(">>>")
if inpt == "anim_runner":
    print("running anim_runner")
    anim_runner()
if inpt == "quit":
    print("exiting...")
    sys.exit()
else:
    print(f"program {inpt} invalid")

