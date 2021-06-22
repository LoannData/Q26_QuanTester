cp -r quanTest/ ./compiled/ 

cd ./compiled/quanTest/
python -m compileall -b 
rm *.py
cd ../../  


cd ./compiled/quanTest/models
python -m compileall -b 
rm *.py
cd ../../../


