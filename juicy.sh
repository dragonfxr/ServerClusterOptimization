rm -rf output/*
for i in {1..6}
do
    python main.py $i
    python cf_output_with_ref.py $i
done

