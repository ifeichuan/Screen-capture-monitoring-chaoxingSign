const express = require('express');
const multer = require('multer');
const path = require('path');
const app = express();

// 设置存储和文件名规则
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        let uploadDir = path.resolve(`./uploads/${req.body.name}`);
if (!fs.existsSync(uploadDir)){
    fs.mkdirSync(uploadDir, { recursive: true });
}

        cb(null, `./uploads/${req.body.name}`);  // 保存到uploads目录
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname);  // 保持原文件名
    }
});

// 创建上传实例
const upload = multer({ storage: storage });

// 创建uploads目录（如果不存在）
const fs = require('fs');
let uploadDir = path.resolve('./uploads');
if (!fs.existsSync(uploadDir)){
    fs.mkdirSync(uploadDir, { recursive: true });
}

// 设置上传处理的路由
app.post('/upload', upload.single('image'), (req, res) => {
    // console.log(req.body);
    
    if (req.file) {
        res.send('File uploaded successfully!');
    } else {
        res.status(400).send('Error: No file uploaded');
    }
});
app.get('/down/:name', (req, res) => {
    res.sendFile(path.join(__dirname, 'uploads', `${req.params.name}//screenhost.png`));
    // res.send("nihao")
})
// 启动服务器
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
