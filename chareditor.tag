<char-editor>
  <table class="chartab">
    <tr each="{ xs, y in model.arr }">
      <td each="{ v, x in xs }" onclick="{ mkclick(x, y) }" class="{ active: v }">
      </td>
    </tr>
  </table>
  
  mkclick(x, y) {
    return function (ev) {
      this.model.set(x, y, !this.model.get(x, y));
      return true;
    }
  } 
  this.model = opts.c;
  
  <style scoped>
    table.chartab { border: 2px solid; background-color: #000; }
    table.chartab td { width: 20px; height: 20px; background-color: #222; padding: 0px;}
    table.chartab td.active { background-color: #fff; }
  </style>
</char-editor>

<char-description>
  <div>
    { model.toByteString(opts.n) }
  </div>
  
  this.model = opts.c;
  this.model.on('changed', function() { riot.update() });
</char-description>