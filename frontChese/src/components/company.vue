<template>
  <el-dialog title="排行榜" :visible.sync="dialogTableVisible" width="40%" :close-on-click-modal=false>
    <el-table :data="boardData">
      <el-table-column property="position" label="排名" width="100"></el-table-column>
      <el-table-column property="id" label="棋局id" width="100"></el-table-column>
      <el-table-column property="name" label="姓名" width="100"></el-table-column>
      <el-table-column property="size" label="棋盘" width="50"></el-table-column>
      <el-table-column property="left" label="剩余棋子" width="100"></el-table-column>

    </el-table>
  </el-dialog>
</template>

<script>
  import qs from 'qs';

  export default {
    name: "company",
    data() {
      return {
        boardData: [],
        rules:"这是游戏规则",
        gridData: [{
          date: '2016-05-02',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          date: '2016-05-04',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          date: '2016-05-01',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          date: '2016-05-03',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }],
        dialogTableVisible: false,
        ruleVisible: false,
        rules:"这就是游戏规则",
      };
    },
    methods: {
      showBoard() {
        this.$http.get('http://127.0.0.1:8000/api/board')
          .then((response) => {
            var res = JSON.parse(response.bodyText);
            if (res.error_num == 0) {
              console.log("board res: ", res.board)
              this.boardData = res.board;
            }
          })

        this.dialogTableVisible = true;
      },

      showRule() {
        this.ruleVisible = true;
        this.rules="这些是规则"
      },
      setBoard(){
        // $emit触发当前实例上的事件
        // 触发父组件的children事件，将this.form回传过去
        this.$emit('board',this.form)
        // 关闭对话框
        this.dialogTableVisible = false
      },
      setRule() {
        this.$emit('rule', this.bodyText)
        this.ruleVisible = false
      }
    },
  }
</script>

<style scoped>
</style>
