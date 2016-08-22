#!/bin/python

import argparse
from skimage import io
import numpy as np
from skimage import transform as tf
from skimage.transform import rotate, rescale

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Regression voting patch cutter')
    parser.add_argument('--pics', required=True, help='Folder containing training pictures')
    parser.add_argument('--kp', required=True, 'Text file containing the filenames and the key points')
    parser.add_arguments('--patches', required=True, 'Folder for patches')
    parser.add_arguments('--N', 'required=True', 'Number of sampling iterations')
    parser.add_arguments('--size', required=True', 'Size of the patch to extract')
    parser.add_arguments('--dmin', required=True, 'Min displacement')
    parser.add_arguments('--dmax', required=True, 'Max displacement')
    parser.add_argument('--rot', required=True, 'Rotation angle [-rot, rot]')
    parser.add_argument('--sc', required=True, 'Scaling factor applied for data augmentation')
    parser.add_argument('--seed', required=True)
    args = parser.parse_args()

    source_dir = args.pics
    points = args.kp
    target_dir = args.patches
    dmin, dmax = args.min, args.dmax
    rot = args.rot
    N_samp = args.N
    S = args.size

    # Setting the seed
    np.random.seed(args.seed)

    # Counter
    cn = 0
    with open(points, 'r') as kp:
        for l in kp:
            fname, points = l.split(':')
            points = tuple(zip(points[0::2], points[1::2]))
            
            I = io.imread(source_dir+'/'+fname)
            I_sc = rescale(I, args.sc)
            I_rot = []
            I_rot_sc = []            
            
            for alpha in range(-rot, rot):
                if alpha != 0:
                    I_rot.append(rotate(I, alpha))
                    I_rot_sc.append(rotate(I_sc, alpha))
            
            
            for p in points:
                # Getting a current center
                x, y = p
                # Generating the centers of the new patches
                for i in range(N):                
                    dx, dy = np.random.randint(dmin, dmax+1), np.random(dmin, dmax+1)
                    if dx+S < I.shape[1] and dx-S >=0:
                        if dy+S < I.shape[0] and dy-S >=0:
                            # Generating a patch SxS
                            cn += 1
                            io.imsave(I[(y+dy-S//2):(y+dy+S//2), x+dx-S//2:x+dx+S//2], target_dir+'/'+'{}_{}_{}.png'.format(cn, x, y))
                            for I_rot_i, I_rot_sc_i in zip(I_rot, I_sc):
                                cn += 1
                                io.imsave(I_rot_i[(y+dy-S//2):(y+dy+S//2), x+dx-S//2:x+dx+S//2], target_dir+'/'+'{}_{}_{}.png'.format(cn, x, y))
                                cn += 1
                                io.imsave(I_rot_sc_i[(y+dy-S//2):(y+dy+S//2), x+dx-S//2:x+dx+S//2], target_dir+'/'+'{}_{}_{}.png'.format(cn, x, y))

             print cn, "patches generated"
            
                     


    
