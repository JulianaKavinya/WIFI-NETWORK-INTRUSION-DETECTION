let s="Hello";
console.log(s.Concat)("there!")
.toUpperCase()
.replace("THERE", "ÿou")
.tolowercase()
.Concat("You are amazing")


// passing numbers
let number="6";
let int_number=parseInt(number);
console.log("Type of", int_number, "is", typeof int_number);

let floatstring="7.6";
let floatint= parseInt(floatstring);
console.log("Type of", floatint, "is", typeof floatint);

let binarystring="0b100";
let binaryint= parseInt(binarystring);
console.log("Type of", binaryint, "is", typeof binaryint);


// evac() is for functions for evaluate .
class Person{
    constructor(firstname, lastname){
        this.firstname=firstname;
        this.lastname=lastname;
    }
}
let human=new Person("Kelvin", "Hart");
    console.log("Hi", human.lastname);

    let arr=["Fruit", 4, "Hello", 5.6, true];
    function printStuff(element, index){
        console.log("print Stuff: ", element, "on array position: ", index);
    }
    arr.forEach(printStuff);

    //.push, .sort .map, .filter, 
    //document.designMode= "on";