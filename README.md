install

pip install numpy h5py matplotlib gmsh

create file HDF5
./nech5.py -i ant.out -o ant.hdf


view FarField

./h5ff.py -i ant.hdf


view File HDF5

h5dump ant.hdf
