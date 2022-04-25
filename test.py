import cv2
import numpy as np

INFILE = "./tiles/rgb/rgb-6.png"
OUTFILE1 = "rot90.png"
OUTFILE2 = "rot180.png"
OUTFILE3 = "rot270.png"
OUTFILE4 = "flip.png"
OUTFILE5 = "flipud.png"
OUTFILE6 = "fliplr.png"

def main():
   print(f"Loading {INFILE}")
   img = cv2.imread(INFILE)

   img1 = np.rot90(img, axes=(1, 0))
   print(f"Saving {OUTFILE1}")
   cv2.imwrite(OUTFILE1, img1)

   img2 = np.rot90(img, 2, axes=(1, 0))
   print(f"Saving {OUTFILE2}")
   cv2.imwrite(OUTFILE2, img2)

   img3 = np.rot90(img, 3, axes=(1, 0))
   print(f"Saving {OUTFILE3}")
   cv2.imwrite(OUTFILE3, img3)

   img4 = np.flip(img, axis=(1, 0))
   print(f"Saving {OUTFILE4}")
   cv2.imwrite(OUTFILE4, img4)

   img5 = np.flipud(img)
   print(f"Saving {OUTFILE5}")
   cv2.imwrite(OUTFILE5, img5)

   img6 = np.fliplr(img)
   print(f"Saving {OUTFILE6}")
   cv2.imwrite(OUTFILE6, img6)

if __name__ == "__main__":
   main()
