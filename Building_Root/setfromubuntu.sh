#!/bin/bash  
###
IAM="`whoami`";
FOLDER="`pwd`";
cd ~;
echo "user=${IAM}"
echo "folder=${FOLDER}"
echo "==================================================================";
echo "=====Installing Progs, Libs and lang-es from repos P1=============";
echo "==================================================================";
#sudo rm -R /software;
sudo rm -rf ~/Shared/MadGraph
/bin/cp /etc/skel/.bashrc ~/
sudo mkdir -p /software/root; 
sudo chown -R "${IAM}" /software;
###sudo sed -i "s/archive.ubuntu.com/mirror.math.princeton.edu/pub/ubuntu/" /etc/apt/sources.list
sudo apt install;
sudo apt update; 
sudo apt -y upgrade;
sudo apt update; 
sudo apt -y upgrade;
sudo apt install;
sudo apt -y install gnome-system-monitor;
sudo apt -y install ssh net-tools git;
sudo snap remove gnome-system-monitor;
sudo apt -y install gnome-system-monitor;
sudo apt -y purge thunderbird*;
sudo apt -y purge ubuntu-web-launchers*;
sudo apt -y install ssh net-tools git;
sudo apt -y install kolourpaint4;
sudo apt -y install gnome-tweak-tool;
sudo apt -y install ubuntu-wallpapers-* edgy-wallpapers feisty-wallpapers gutsy-wallpapers;
sudo apt -y install wine-stable;
sudo apt -y install vlc;
sudo apt -y install nautilus-dropbox;
sudo nautilus --quit;
sudo apt -y install libappindicator1;
sudo ubuntu-drivers autoinstall
sudo apt purge firefox;
#wget -c https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt install;
sudo apt update; 
sudo apt -y upgrade;
sudo apt update; 
sudo apt -y upgrade;
sudo apt install;
cd ~;
###wget https://raw.githubusercontent.com/mercutiodesign/texmaker-3.3.3/master/dictionaries/es_ES.dic
###wget https://raw.githubusercontent.com/mercutiodesign/texmaker-3.3.3/master/dictionaries/es_ES.aff


echo "==================================================================";
echo "=====Installing Progs, Libs and lang-es from repos P2=============";
echo "==================================================================";
sudo sh -c "sudo bash -x '${FOLDER}'/progs.sh"
###
echo "=================================================================="
echo "====================Installing ROOT/C++==========================="
echo "=================================================================="
echo "Desea Instalar ROOT/C++? (y/n)"

read askk

while [ $askk != "y" ] && [ $askk != "n" ]
do
    clear
    echo "Desea Instalar ROOT/C++? (y/n)"
    read askk
done

if [ $askk == "y" ]
then
	#sudo apt update; 
	#cd /software; 
	#git clone https://github.com/Kitware/CMake cmake;
	#sudo apt update; 
	#cd cmake;time ./bootstrap; make -j `nproc`; sudo make install; 

    cd /software/root; 
    git clone https://github.com/root-project/root source; cd source;
    ./configure --build=debug --enable-roofit --enable-minuit2 --enable-builtin-freetype;
    cd ..;     mkdir build; cd build; 
    cmake -DCMAKE_INSTALL_PREFIX=../install -DPython3_EXECUTABLE=python3 -DPython2_EXECUTABLE=python -Dxrootd=OFF -Dbuiltin_xrootd=OFF ../source/;
    make -j `nproc`; make test; make install;
    TOOLS=/software;
    export ROOT_DIR=${TOOLS}/root/install; 
    export ROOT_INCLUDE_DIR=${ROOT_DIR}/include/;
    export ROOT_LIBRARY=${ROOT_DIR}/lib/;
    export LD_LIBRARY_PATH=${ROOT_LIBRARY}:${LD_LIBRARY_PATH}; 
    export PATH=$ROOT_DIR/bin/:$PATH; 
    source ${ROOT_DIR}/bin/thisroot.sh;
	
	./configure linuxdeb2 --with-thread=/usr/lib/libpthread.so
	gmake depend
	gmake

    
    echo "=================================================================="
    echo "======================Installing CLHEP============================"
    echo "=================================================================="
    cd /software;
    mkdir clhep; cd clhep; 
    git clone https://gitlab.cern.ch/CLHEP/CLHEP.git source; 
    mkdir build; cd build; 
    cmake -DCMAKE_INSTALL_PREFIX=../install ../source/; 
    make -j `nproc`; make test; make install;
    TOOLS=/software; 
    export CLHEP_DIR=${TOOLS}/clhep/install; 
    export CLHEP_INCLUDE_DIR=${CLHEP_DIR}/include/;
    export CLHEP_LIBRARY=${CLHEP_DIR}/lib/; 
    export LD_LIBRARY_PATH=${CLHEP_LIBRARY}:${LD_LIBRARY_PATH}; 
    export PATH=$CLHEP_DIR/bin/:$PATH; 
    echo "=================================================================="
    echo "======================Installing Geant4==========================="
    echo "=================================================================="
    cd /software; mkdir geant; cd geant; 
    git clone https://gitlab.cern.ch/geant4/geant4.git source; 
    mkdir build; cd build;
    cmake -DCMAKE_INSTALL_PREFIX=../install -DGEANT4_INSTALL_DATA=ON -DGEANT4_USE_QT=ON -DGEANT4_USE_OPENGL_X11=ON -DGEANT4_USE_RAYTRACER_X11=ON -DGEANT4_USE_GDML=ON -DGEANT4_BUILD_MULTITHREADED=ON -DGEANT4_USE_SYSTEM_CLHEP=ON ../source; 
    make -j `nproc`;  make test; make install;
    TOOLS=/software; 
    export GEANT4_DIR=${TOOLS}/geant/install; 
    export GEANT4_INCLUDE_DIR=${GEANT4_DIR}/include/;
    export GEANT4_LIBRARY=${GEANT4_DIR}/lib/;
    export LD_LIBRARY_PATH=${GEANT4_LIBRARY}:${LD_LIBRARY_PATH}; 
    export PATH=$GEANT4_DIR/bin/:$PATH; 
    source ${GEANT4_DIR}/bin/geant4.sh;
	echo "=================================================================="
    echo "===================Installing FastJet3.3.4========================"
    echo "=================================================================="
    cd /software; mkdir FastJet; cd FastJet; 
	wget http://fastjet.fr/repo/fastjet-3.3.4.tar.gz; tar zxvf fastjet-3.3.4.tar.gz;
	mkdir source; mv fastjet-3.3.4/* source; rm -rf fastjet-3.3.4; cd source;
	./configure --prefix=$PWD/../install --enable-allplugins --enable-pyext;
    make -j `nproc`;  make check; make install;
    TOOLS=/software; 
    export FASTJET_DIR=${TOOLS}/FastJet/install;
    export FASTJET_INCLUDE_DIR=${FASTJET_DIR}/include/;
    export FASTJET_LIBRARY=${FASTJET_DIR}/lib/;
    export LD_LIBRARY_PATH=${FASTJET_LIBRARY}:${LD_LIBRARY_PATH};
    export PATH=$FASTJET_DIR/bin/:$PATH; 
	
	pip install jupyter
	pip install jupyterhub
	pip install metakernel
	
	cd ${FOLDER}
	tar -xzvf ${FOLDER}/MG5_aMC_v2.9.4.tar.gz -C /software/
	
    rm -rf ~/Shared/MadGraph
	mkdir -p ~/Shared/MadGraph 
	ln -s /software/MG5_aMC_v2_9_4 ~/Shared/MadGraph
	
	tar -xzvf ${FOLDER}/MadAnalysis5.tgz -C /software/MG5_aMC_v2_9_4/
	
	
    echo "=================================================================="
    echo "=========================Setting bashrc==========================="
    echo "=================================================================="
    sudo chown -R "${IAM}" ~/.bashrc;

	echo "madgraph () {" >> ~/.bashrc;
	echo "cd ~/Shared/MadGraph && ./MG5_aMC_v2_9_4/bin/mg5_aMC" >> ~/.bashrc;
	echo "}" >> ~/.bashrc;
	
	echo "madanalysis () {" >> ~/.bashrc;
	echo "cd ~/Shared/MadGraph && ./MG5_aMC_v2_9_4/madanalysis5/bin/ma5" >> ~/.bashrc;
	echo "}" >> ~/.bashrc;
	
	echo "madfolder () {" >> ~/.bashrc;
	echo "cd ~/Shared/MadGraph" >> ~/.bashrc;
	echo "}" >> ~/.bashrc;
	
	echo "alias execmadgraph=./MG5_aMC_v2_9_4/bin/mg5_aMC" >> ~/.bashrc;
	echo "alias execmadanalysis=./MG5_aMC_v2_9_4/madnalysis5/bin/ma5" >> ~/.bashrc;

    TOOLS=/software; 
    export ROOT_DIR=${TOOLS}/root/install; 
    export ROOT_INCLUDE_DIR=${ROOT_DIR}/include/;
    export ROOT_LIBRARY=${ROOT_DIR}/lib/;
    export LD_LIBRARY_PATH=${ROOT_LIBRARY}:${LD_LIBRARY_PATH}; 
    export PATH=$ROOT_DIR/bin/:$PATH; 
    source ${ROOT_DIR}/bin/thisroot.sh;
    export CLHEP_DIR=${TOOLS}/clhep/install; 
    export CLHEP_INCLUDE_DIR=${CLHEP_DIR}/include/;
    export CLHEP_LIBRARY=${CLHEP_DIR}/lib/; 
    export LD_LIBRARY_PATH=${CLHEP_LIBRARY}:${LD_LIBRARY_PATH}; 
    export PATH=$CLHEP_DIR/bin/:$PATH; 
    export GEANT4_DIR=${TOOLS}/geant/install; 
    export GEANT4_INCLUDE_DIR=${GEANT4_DIR}/include/;
    export GEANT4_LIBRARY=${GEANT4_DIR}/lib/;
    export LD_LIBRARY_PATH=${GEANT4_LIBRARY}:${LD_LIBRARY_PATH}; 
    export PATH=$GEANT4_DIR/bin/:$PATH; 
    source ${GEANT4_DIR}/bin/geant4.sh;
	export FASTJET_DIR=${TOOLS}/FastJet/install;
    export FASTJET_INCLUDE_DIR=${FASTJET_DIR}/include/;
    export FASTJET_LIBRARY=${FASTJET_DIR}/lib/;
    export LD_LIBRARY_PATH=${FASTJET_LIBRARY}:${LD_LIBRARY_PATH};
    export PATH=$FASTJET_DIR/bin/:$PATH; 
	export PYTHONPATH=${PYTHONPATH}:`fastjet-config --pythonpath`;

    echo "TOOLS=/software; " >> ~/.bashrc;
    echo "export ROOT_DIR=${TOOLS}/root/install; " >> ~/.bashrc;
    echo "export ROOT_INCLUDE_DIR=${ROOT_DIR}/include/;" >> ~/.bashrc;
    echo "export ROOT_LIBRARY=${ROOT_DIR}/lib/;" >> ~/.bashrc;
    echo "export LD_LIBRARY_PATH=${ROOT_LIBRARY}:${LD_LIBRARY_PATH}; " >> ~/.bashrc;
    echo "export PATH=$ROOT_DIR/bin/:$PATH;" >> ~/.bashrc; 
    echo "source ${ROOT_DIR}/bin/thisroot.sh;" >> ~/.bashrc;
    echo "export CLHEP_DIR=${TOOLS}/clhep/install;" >> ~/.bashrc; 
    echo "export CLHEP_INCLUDE_DIR=${CLHEP_DIR}/include/;" >> ~/.bashrc;
    echo "export CLHEP_LIBRARY=${CLHEP_DIR}/lib/;" >> ~/.bashrc; 
    echo "export LD_LIBRARY_PATH=${CLHEP_LIBRARY}:${LD_LIBRARY_PATH}; " >> ~/.bashrc;
    echo "export PATH=$CLHEP_DIR/bin/:$PATH; " >> ~/.bashrc;
    echo "export GEANT4_DIR=${TOOLS}/geant/install; " >> ~/.bashrc;
    echo "export GEANT4_INCLUDE_DIR=${GEANT4_DIR}/include/;" >> ~/.bashrc;
    echo "export GEANT4_LIBRARY=${GEANT4_DIR}/lib/;" >> ~/.bashrc;
    echo "export LD_LIBRARY_PATH=${GEANT4_LIBRARY}:${LD_LIBRARY_PATH}; " >> ~/.bashrc;
    echo "export PATH=$GEANT4_DIR/bin/:$PATH; " >> ~/.bashrc;
    echo "source ${GEANT4_DIR}/bin/geant4.sh;" >> ~/.bashrc;
	echo "export FASTJET_DIR=${TOOLS}/FastJet/install; " >> ~/.bashrc;
    echo "export FASTJET_INCLUDE_DIR=${FASTJET_DIR}/include/;" >> ~/.bashrc;
    echo "export FASTJET_LIBRARY=${FASTJET_DIR}/lib/;" >> ~/.bashrc;
    echo "export LD_LIBRARY_PATH=${FASTJET_LIBRARY}:${LD_LIBRARY_PATH}; " >> ~/.bashrc;
    echo "export PATH=$FASTJET_DIR/bin/:$PATH; " >> ~/.bashrc;
	echo "export PYTHONPATH=${PYTHONPATH}:`fastjet-config --pythonpath`; " >> ~/.bashrc;
    sudo chown -R "${IAM}" /software;
fi

sudo reboot
