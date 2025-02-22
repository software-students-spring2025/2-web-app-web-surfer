const express = require('express');
const mongoose = require('mongoose');
const app = express();

// 连接MongoDB
mongoose.connect('mongodb://admin:your_password@localhost:27017/your_database', {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => {
  console.log('MongoDB连接成功');
})
.catch((err) => {
  console.error('MongoDB连接错误:', err);
});

// 中间件
app.use(express.json());

// 路由
app.use('/api', require('./routes/register'));

// 启动服务器
const PORT = process.env.PORT || 5001;
app.listen(PORT, () => {
  console.log(`服务器运行在端口 ${PORT}`);
});