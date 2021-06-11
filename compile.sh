cd quanTest 
cp *.py ../compiled/quanTest/
cd ../compiled/quanTest/
python -m compileall -b 
rm *.py 
cd ../../
