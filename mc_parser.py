import anvil # https://pypi.org/project/anvil-parser/ 
import math

try:
    region = anvil.Region.from_file('r.0.0.mca') # region file(needs to be in the same folder)
except Exception:
    print("The region file cant be found")
    exit()

RegionX = 0 # region coordinates of the file (r.X.Z.mca)
RegionZ = 0

cBlocks = [["grass",0,0,0],["dirt",0,-1,0],["stone",1,1,0],["stone",1,2,0]] # blocks to check(Offs are relative to 0,0,0 block) [id,xOff,yOff,zOff]

ymin = 62 # range for y coordinates of the search
ymax = 63

# =====

chunk = 0
outs = []

for cX in range(32):
    for cZ in range(32):
        do = True
        try:
            chunk = anvil.Chunk.from_region(region, cX, cZ)
        except Exception:
            do = False
            print("Skipped chunk: " + str(cX) + ", " + str(cZ))
        if(do):
            print("Chunk: " + str(cX) + ", " + str(cZ))
            for x in range(16):
                for y in range(ymin,ymax):
                    for z in range(16):
                        isThere = 0
                        for i in cBlocks:
                            noChunk = False
                            if x+i[1] > 15 or x+i[1] < 0 or z+i[3] > 15 or z+i[3] < 0:
                                try:
                                    chunk = anvil.Chunk.from_region(region, cX + math.floor((i[1]+x)/16), cZ + math.floor((i[3]+z)/16))
                                except Exception:
                                    print("Skipped reloading chunk",cX + math.floor((i[1]+x)/16), cZ + math.floor((i[3]+z)/16))
                                    noChunk = True
                            
                            if not noChunk:
                                try:
                                    block = chunk.get_block((x+i[1]) % 16, y+i[2], (z+i[3]) % 16)
                                    if block.id == i[0]:
                                        isThere += 1
                                except Exception:
                                    print(x+i[1], y+i[2], z+i[3])
                        if isThere >= len(cBlocks):
                            Rx = x + RegionX*32*16 + cX * 16
                            Rz = z + RegionZ*32*16 + cZ * 16

                            s = "Found at: x:" + str(Rx) + ", y: " + str(y) + ", z: " + str(Rz)
                            print(s)
                            outs.append(s)

print("Summary: ")

if len(outs) > 0:
    for i in outs:
        print(i)
else:
    print("Nothing Found :(")
