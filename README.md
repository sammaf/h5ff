install

pip install numpy h5py matplotlib gmsh

create file HDF5
./nech5.py -i ant.out -o ant.hdf


viev FarField

./h5ff.py -i ant.hdf
