cp dist/static/static/note-1020/note.pickle ../static/note-1020
cd client
npm run build
cd ../
cp -r ../static dist/static
python app.py