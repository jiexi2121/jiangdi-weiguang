const { execSync } = require('child_process');

// 使用 google-chrome 无头模式截图
const slides = [
  { file: '江底微光_版本A.html', id: 'slide1', output: '江底微光_版本A_封面.png' },
  { file: '江底微光_版本A.html#slide2', id: 'slide2', output: '江底微光_版本A_引语.png' },
  { file: '江底微光_版本A.html#slide3', id: 'slide3', output: '江底微光_版本A_核心.png' },
  { file: '江底微光_版本A.html#slide4', id: 'slide4', output: '江底微光_版本A_结尾.png' },
  { file: '江底微光_版本B.html', id: 'slideB1', output: '江底微光_版本B_封面.png' },
  { file: '江底微光_版本B.html#slideB2', id: 'slideB2', output: '江底微光_版本B_引语.png' },
  { file: '江底微光_版本B.html#slideB3', id: 'slideB3', output: '江底微光_版本B_核心.png' },
  { file: '江底微光_版本B.html#slideB4', id: 'slideB4', output: '江底微光_版本B_结尾.png' },
];

console.log('开始截图...');
