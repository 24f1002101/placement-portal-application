<script setup>
import { ref } from 'vue'
import router from '@/router'
const naam = ref('')
const email = ref('')
const password = ref('')
const role = ref('')
const branch = ref('')
const cgpa = ref('')
const year = ref('')
const company_naam = ref('')
const hr_contanct = ref('')
const website = ref('')
const validate = function(){
    console.log(email.value)
    console.log(password.value)
    if(!email.value.includes('@gmail.com')){
        alert('Please enter valid email to Login !!!')
        return false
    }
    if(password.value.length<6){
        alert('Please enter the password with length greater than 6 !!!')
        return false
    }
    if(role.value==='student'){
        if(year.value>4 || year.value<1){
            alert('Please enter valid year !!!')
                    return false
        }

    }
    if(role.value==='student'){
        if(cgpa.value>10 || cgpa.value<5){
            alert('Please enter valid CGPA !!!')
               return false
        }
     
    }
    if(role.value==='company'){
        if(String(hr_contanct.value).length!==10){
            alert('check the length of phone number !!!')   
             return false
        }
       
    }
    const small = 'abcdefghijklmnopqrstuvwxyz'
    const large = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    const numbers = '1234567890'
    const special = '~!@#$%^&*()_+{}[];:,.<>?/'
    
    let count_small = 0
    let count_large = 0
    let count_numbers = 0
    let count_special = 0

    for(let i=0;i<password.value.length;i++){
        if(small.includes(password.value[i])){
            count_small +=1
        }
        if(large.includes(password.value[i])){
            count_large +=1
        }
        if(numbers.includes(password.value[i])){
            count_numbers +=1
        }
        if(special.includes(password.value[i])){
            count_special +=1
        }
    }
    if(count_small>=1 && count_large>=1 && count_numbers>=1 && count_special>=1 && password.value.length>=6){
        return true
    }
    else{
        if(count_small<1){
            alert('Password should contain a small Alphabet !!!')
            return false
        }
        if(count_large<1){
            alert("Password should contain a Capital Alphabet !!!")
            return false
        }
        if(count_numbers<1){
            alert("Password should contain a Numerical digit !!!")
            return false
        }
        if(count_special<1){
            alert("Password should contain a special character !!!")
            return false
        }
    }

}

async function check(){
    const ans = validate()
    if(ans){
        if(role.value=='student'){
            const input = {
                name : naam.value,
                email : email.value,
                password : password.value,
                branch : branch.value,
                cgpa : cgpa.value,
                year : year.value
            }
            const response = await fetch('http://127.0.0.1:5000/api/student_register',{
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body : JSON.stringify(input)
            })
            if(!response.ok){
                const result = await response.json()
                alert(result.message)
            }
            else{
                const result = await response.json()
                alert(result.user_name + "successfully registered !!!")
                router.push('/')
                
            }
        }
    
        else if(role.value=='company'){
        const input = {
            name : naam.value,
            email : email.value,
            password : password.value,
            company_name : company_naam.value,
            hr_contact : hr_contanct.value,
            website : website.value
        }
        const response = await fetch('http://127.0.0.1:5000/api/company_register',{
            method : "POST",
            headers:{
                "Content-Type":"application/json"
            },
            body : JSON.stringify(input)
        })
        if(!response.ok){
            const result = await response.json()
            alert(result.message)
        }
        else{
            const result = await response.json()
            alert(result.user_name + "successfully registered !!!")
            router.push('/')
        }
        }
    }
}

</script>

<template>
    <div>
        <form @submit.prevent="check">
            Name:<input type="text" required v-model="naam">
            Email:<input type="text" required v-model="email">
            password:<input type="password" required v-model="password">
            Role:
            <select v-model="role">
                <option value="student">Student</option>
                <option value="company">Company</option>
            </select>
            <p v-if="role=='student'">Branch:</p><input type="text" required v-model="branch" v-if="role=='student'">
            <p v-if="role=='student'">Cgpa:</p><input type="number" required v-model="cgpa" step="any" v-if="role=='student'">
            <p v-if="role=='student'">Year:</p><input type="number" required v-model="year" v-if="role=='student'">
            <p v-if="role=='company'">Company Name:</p><input type="text" required v-model="company_naam" v-if="role=='company'">
            <p v-if="role=='company'">HR Contact:</p><input type="number" required v-model="hr_contanct" v-if="role=='company'">
            <p v-if="role=='company'">Website Associated:</p><input type="text" required v-model="website" v-if="role=='company'">
            <input type="submit" value="sumbit">
        </form>
    </div>
</template>

<style scoped>

</style>