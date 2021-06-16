function doSomething(){
    let aV = document.getElementById('inputA').value;
    let bV = document.getElementById('inputB').value;
    document.getElementById('valueA').innerHTML = aV;
    document.getElementById('valueB').innerHTML = bV;
    document.getElementById('valueC').innerHTML = Number(aV) + Number(bV);
}