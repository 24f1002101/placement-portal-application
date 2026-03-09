<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/counter'
import router from '@/router'
import { defineProps } from 'vue'
import CompanyDashboard from './CompanyDashboard.vue'
const mail = ref('')
const password = ref('')
const selectedvalue = ref('')
const auth_store = useAuthStore()
const error_value = ref('')
const HandleSubmit = function(){
    console.log(mail.value)
    console.log(password.value)
    if(!mail.value.includes('@gmail.com')){
        alert('Please enter valid email to Login !!!')
        return false
    }
    if(password.value.length<6){
        alert('Please enter the password with length greater than 6 !!!')
        return false
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

async function validate(){
    const ans = HandleSubmit()
    if(ans){
            if(selectedvalue.value === 'admin'){
                const user = {
                    email : mail.value,
                    password : password.value
                }
                const response = await fetch("http://127.0.0.1:5000/api/user_login",{
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json"
                },
                body: JSON.stringify(user)
                })
                if(!response.ok){
                    const error_message = await response.json()
                    alert('Login Failed !!!'+ error_message.message)
                }
                else{
                    const output = await response.json()
                    console.log(output.auth_token)
                    const user1 = {
                        email : mail.value,
                        password : password.value,
                        name : output.name
                    }
                    auth_store.setUserCred(output.auth_token,user1)
                    console.log(selectedvalue.value)
                    router.push('/admin_dashboard')
                }
            }
            else if(selectedvalue.value === 'student'){
                const user = {
                    email : mail.value,
                    password : password.value
                }
                const response = await fetch("http://127.0.0.1:5000/api/user_login",{
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json"
                },
                body: JSON.stringify(user)
                })
                if(!response.ok){
                    const error_message = await response.json()
                    alert('Login Failed !!!'+ error_message.message)
                }
                else{
                    const output = await response.json()
                    console.log(output.auth_token)
                    const user1 = {
                        email : mail.value,
                        password : password.value,
                        name : output.name,
                        status : output.status
                    }
                    auth_store.setUserCred(output.auth_token,user1)
                    console.log(selectedvalue.value)
                    router.push('/student_dashboard')
                }
            }
            else if(selectedvalue.value === 'company'){
                const user = {
                    email : mail.value,
                    password : password.value
                }
                const response = await fetch("http://127.0.0.1:5000/api/user_login",{
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json"
                },
                body: JSON.stringify(user)
                })
                if(!response.ok){
                    const error_message = await response.json()
                    alert('Login Failed !!!'+ error_message.message)
                }
                else{
                    const output = await response.json()
                    console.log(output.auth_token)
                    const user1 = {
                        email : mail.value,
                        password : password.value,
                        name : output.name,
                        status : output.status
                    }
                    auth_store.setUserCred(output.auth_token,user1)
                    console.log(selectedvalue.value)
                    router.push('/company_dashboard')
                }
            }
        }
    }


</script>

<template>
    <div>
        <form @submit.prevent="validate">
            Email:<input type="text" name="email" id="email" required v-model="mail">
            Password:<input type="password" name="password" id="password" required v-model="password">
            Role:<select v-model="selectedvalue">
                <option value="admin">Admin</option>
                <option value="student">Student</option>
                <option value="company">Company</option>
            </select>
            <input type="submit" value="submit">
        </form>
        <RouterLink to="/register"><p v-if="selectedvalue!='admin'">Go to register</p></RouterLink>
        
    </div>
</template>

<style scoped>

</style>