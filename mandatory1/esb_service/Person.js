module.exports = class Person{
    constructor(name, email, phone, gender){
        this.name = name;
        this.email = email;
        this.phone = phone;
        this.gender = gender;
    }

    Visualize(){
        console.log(`Name: ${this.name}, Email: ${this.email}, Phone: ${this.phone}, Gender: ${this.gender}`);
    }
};