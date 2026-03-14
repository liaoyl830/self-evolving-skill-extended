#!/usr/bin/env node
/**
 * Self-Evolving Skill 测试脚本
 */

const fs = require('fs');
const path = require('path');

const STORAGE_DIR = process.argv[2] || path.join(process.env.APPDATA || process.env.HOME || '', '.openclaw', 'self-evolving-skill', 'storage');
const SKILLS_FILE = path.join(STORAGE_DIR, 'skills.json');

console.log('Self-Evolving Skill 测试');
console.log('========================\n');
console.log(`存储目录：${STORAGE_DIR}`);
console.log(`技能文件：${SKILLS_FILE}\n`);

// 确保存储目录存在
if (!fs.existsSync(STORAGE_DIR)) {
  console.log('创建存储目录...');
  fs.mkdirSync(STORAGE_DIR, { recursive: true });
}

// 初始化或加载技能文件
let data = { skills: [], experiences: [], stats: { totalExecutions: 0, totalReflections: 0, totalMutations: 0, valueGateAccepted: 0 } };
if (fs.existsSync(SKILLS_FILE)) {
  try {
    data = JSON.parse(fs.readFileSync(SKILLS_FILE, 'utf-8'));
    console.log('✓ 已加载现有技能数据\n');
  } catch (e) {
    console.log('⚠ 无法读取技能文件，将创建新文件\n');
  }
}

// 测试：创建技能
function createSkill(name) {
  const skill = {
    id: `skill_${Date.now()}`,
    name: name,
    description: '',
    createdAt: new Date().toISOString(),
    executionCount: 0,
    successCount: 0,
    totalValue: 0
  };
  
  data.skills.push(skill);
  saveData();
  
  console.log(`✓ 创建技能：${skill.id}`);
  console.log(`  名称：${skill.name}`);
  console.log(`  创建时间：${skill.createdAt}\n`);
  
  return skill;
}

// 测试：列出技能
function listSkills() {
  console.log(`技能列表 (${data.skills.length}):\n`);
  data.skills.forEach(skill => {
    console.log(`  - ${skill.id}: ${skill.name}`);
    console.log(`    执行次数：${skill.executionCount}, 成功：${skill.successCount}`);
  });
  console.log('');
}

// 测试：执行技能
function executeSkill(skillId, success = true, value = 1.0) {
  const skill = data.skills.find(s => s.id === skillId);
  if (!skill) {
    console.log(`✗ 未找到技能：${skillId}\n`);
    return false;
  }
  
  skill.executionCount++;
  if (success) skill.successCount++;
  skill.totalValue += value;
  
  data.stats.totalExecutions++;
  if (success) data.stats.valueGateAccepted++;
  
  // 添加经验
  data.experiences.push({
    skillId,
    timestamp: new Date().toISOString(),
    success,
    value,
    context: {}
  });
  
  saveData();
  
  console.log(`✓ 执行技能：${skillId}`);
  console.log(`  成功：${success}`);
  console.log(`  价值：${value}`);
  console.log(`  累计执行：${skill.executionCount}\n`);
  
  return true;
}

// 测试：统计
function showStats() {
  console.log('系统统计:');
  console.log(`  技能数：${data.skills.length}`);
  console.log(`  经验数：${data.experiences.length}`);
  console.log(`  总执行：${data.stats.totalExecutions}`);
  console.log(`  反思触发：${data.stats.totalReflections}`);
  console.log(`  变异数：${data.stats.totalMutations}`);
  console.log(`  价值门接受率：${data.stats.totalExecutions > 0 ? ((data.stats.valueGateAccepted / data.stats.totalExecutions) * 100).toFixed(1) : 0}%\n`);
}

// 保存数据
function saveData() {
  fs.writeFileSync(SKILLS_FILE, JSON.stringify(data, null, 2), 'utf-8');
}

// 命令行参数处理
const command = process.argv[3];

switch (command) {
  case 'create':
    createSkill(process.argv[4] || 'TestSkill');
    break;
  case 'list':
    listSkills();
    break;
  case 'execute':
    executeSkill(process.argv[4] || data.skills[0]?.id, true, 0.8);
    break;
  case 'stats':
    showStats();
    break;
  default:
    console.log('用法: node test.js [create|list|execute|stats] [args...]');
    console.log('\n示例:');
    console.log('  node test.js create "MySkill"  - 创建技能');
    console.log('  node test.js list              - 列出技能');
    console.log('  node test.js execute skill_123 - 执行技能');
    console.log('  node test.js stats             - 查看统计');
    console.log('');
    
    // 默认显示列表
    listSkills();
}
