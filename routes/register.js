const express = require('express');
const router = express.Router();
const User = require('../models/User');

router.post('/register', async (req, res) => {
  try {
    console.log('收到的注册数据:', req.body);

    // 验证数据格式
    const { username, email, password, isAdmin } = req.body;
    
    if (!username || typeof username !== 'string') {
      return res.status(400).json({
        success: false,
        message: '用户名格式不正确'
      });
    }

    if (!email || !email.includes('@')) {
      return res.status(400).json({
        success: false,
        message: '邮箱格式不正确'
      });
    }

    if (!password || typeof password !== 'string') {
      return res.status(400).json({
        success: false,
        message: '密码格式不正确'
      });
    }

    // 创建用户对象
    const newUser = new User({
      username: username.trim(),
      email: email.trim().toLowerCase(),
      password,
      isAdmin: Boolean(isAdmin)
    });

    console.log('准备保存的用户数据:', newUser);

    // 保存到数据库
    const savedUser = await newUser.save();
    console.log('保存成功:', savedUser);

    res.status(201).json({
      success: true,
      message: '注册成功'
    });

  } catch (error) {
    console.error('注册错误:', error);
    res.status(500).json({
      success: false,
      message: '注册失败，请重试',
      error: error.message
    });
  }
});

module.exports = router; 