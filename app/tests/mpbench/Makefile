all:
	wget http://icl.cs.utk.edu/projects/llcbench/llcbench.tar.gz
	tar -xvf llcbench.tar.gz
	cd llcbench && make linux-mpich
	cp sys.linux-mpich llcbench/conf
	cp hostfile llcbench/mpbench/
	cd llcbench && make mp-run 

clean:
	rm -rf llcbench*
	rm -rf *~
