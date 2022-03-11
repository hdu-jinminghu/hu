<!--
 * @Author: your name
 * @Date: 2021-08-16 14:17:40
 * @LastEditTime: 2021-12-28 15:36:12
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \frontend\src\App.vue
-->

<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>

export default{
  components: {
  }
}
</script>

<style lang='less' scoped>
#app {
  /* // font-family: 'Avenir', Helvetica, Arial, sans-serif; */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0;
  padding: 0;
  display: flex;
  height: 100%;
  user-select: none;
  /* // font-family: "Arial","Microsoft YaHei","黑体","宋体",sans-serif;; */
  ::-webkit-scrollbar {
      width: 5px;
      height: 5px;
      background-color: white;
    }
    /*定义滚动条轨道 内阴影+圆角*/
    ::-webkit-scrollbar-track{
      box-shadow: inset 0 0 6px rgba(0,0,0,0.1);
      border-radius: 0px;
    }
    /*定义滑块 内阴影+圆角*/
    ::-webkit-scrollbar-thumb{
      border-radius: 10px;
      /*-webkit-box-shadow: inset 0 0 6px rgba(0,0,0,.3);*/
      background-color: #ccc;
    }
}
</style>
