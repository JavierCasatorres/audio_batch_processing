import sys
import argparse
import numpy as np
from pathlib import Path
from pydub import AudioSegment
parser = argparse.ArgumentParser(description='Process an mp3 file.')
parser.add_argument('infile', nargs='?', type=str, default=None)
parser.add_argument('outfolder', nargs='?', type=str,
                    default="./output")
parser.add_argument('--op', nargs=1, default="chop", help="Define operation to perform")
parser.add_argument('--chop_size', nargs=1, default=10000, help="Size of each audio chunk in ms")
parser.add_argument('--out_format', nargs=1, default="mp3", help="Output format for the chunks")
args = parser.parse_args()
if args.infile is None:
    raise ValueError("No audio file specified")
file = Path(args.infile)
outfolder = Path(args.outfolder)
try:
    outfolder.mkdir(exist_ok=True)
except FileNotFoundError:
    raise FileNotFoundError("Missing folder parents")
if "chop" in args.op:
    print(f"Loading {args.infile}...")
    audio = AudioSegment.from_mp3(args.infile)
    print("Done. Processing")
else:
    raise ValueError("Option not implemented")
nchunks = int(np.ceil(len(audio)/10000))
completion = list(np.linspace(0, nchunks, num=100).astype('int'))
for chunk in range(nchunks):
    if chunk in completion:
        print(f"{completion.index(chunk)}% completed")
    audio[chunk*args.chop_size:((chunk+1)*args.chop_size)].export(outfolder / Path(file.stem + f"_chunk{str(chunk).zfill(4)}.{args.out_format}"), format=args.out_format)   
print(f"File chopped succesfully, {nchunks} fragments"
      f" of {args.chop_size/1000} seconds each")
