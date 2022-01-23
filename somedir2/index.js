const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const routes = require("./server/routes");

// const multer = require ("multer");
// const fileStorageEngine = multer.diskStorage({
//   destination: (req, file, cb) =>{
//     cb(null, './images')},
//     filename:(req, file, cb) =>{
//       cb(null,Date.now() + '--' + file.originalname)
//     }
// });
// const upload = multer({storage:fileStorageEngine})

// app.post('/userprofiles/image',upload.single('picture'),(req, res)=>{
//   console.log(req.file);
//   res.send('Image upload Successfully');
// })

app.use(bodyParser.urlencoded({ extended: false, limit: '5mb' }));
app.use(bodyParser.json());
app.use("/", routes);

const server = app.listen(3000, "localhost", function () {
  console.log(`Blog App listening at http://localhost:${3000}`);
});