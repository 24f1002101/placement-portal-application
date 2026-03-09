<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import { useAuthStore } from '@/stores/counter';
import router from '@/router';
const auth_store = useAuthStore()
const mail = ref(JSON.parse(localStorage.getItem('user'))?.email || null)
const auth_token = auth_store.getAuthToken()
const password = ref(JSON.parse(localStorage.getItem('user'))?.password || null)
const year = ref(0)
const branch = ref('')
const name = ref('')
const cgpa = ref(3.45)
const email = ref('')
async function fetchStudentDetails(){
    const input = {
        email : mail.value
    }
    const response = await fetch('http://127.0.0.1:5000/api/display_necessary_information',{
        method : "POST",
        headers :{
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        },
        body : JSON.stringify(input)
    })
    if(response.ok){
        const output = await response.json()
        year.value = output.year
        branch.value = output.branch
        email.value = mail.value
        name.value = output.name
        cgpa.value = output.cgpa
    }
}
onMounted(()=>{
    fetchStudentDetails()
})

const HandleSubmit = function(){
    if(!email.value.includes('@gmail.com')){
        alert('Please enter valid email to Login !!!')
        return false
    }
    if(cgpa.value<6 || cgpa.value>10){
        alert("please enter cgpa between 6 to 10 !!!")
        return false
    }
    if(year.value<1 || year.value>4){
        alert("please check year it should be between 1 to 4 !!!")
        return false
    }
    return true
}

async function validity_check(){
    const ans = HandleSubmit()
    if(ans===true){
        const input = {
            original_email : mail.value,
            name : name.value,
            changing_email : email.value,
            branch : branch.value,
            year : year.value,
            cgpa : cgpa.value
        }
        const response = await fetch("http://127.0.0.1:5000/api/edit_profile_student",{
            method : "POST",
            headers : {
                "Content-Type" : "application/json",
                "Authentication-Token" : auth_token
            },
            body : JSON.stringify(input)
        })
        if(response.ok){
            const output = await response.json()
            const user1 = {
                email : email.value,
                password : password.value,
                name : output.name,
                status : output.status
            }
            auth_store.setUserCred(auth_token,user1)
            alert("Successfully Updated The Details Of Yours !!!")
            router.push('/student_dashboard')
        }
        else{
            const output = await response.json()
            alert(output.message)
        }
    }
}
</script>

<template>
    <div class="container mt-5">
        <div class="card p-4 shadow-sm" style="max-width: 500px; margin: auto;">
            <h5 class="fw-bold mb-4">Edit Profile</h5>
            <form @submit.prevent="validity_check">

                <div class="mb-3">
                    <label class="form-label fw-semibold">Name</label>
                    <input type="text" class="form-control" v-model="name" />
                </div>

                <div class="mb-3">
                    <label class="form-label fw-semibold">Email</label>
                    <input type="text" class="form-control" v-model="email" />
                </div>

                <div class="mb-3">
                    <label class="form-label fw-semibold">Year</label>
                    <input type="number" class="form-control" v-model="year" />
                </div>

                <div class="mb-3">
                    <label class="form-label fw-semibold">Branch</label>
                    <input type="text" class="form-control" v-model="branch" />
                </div>

                <div class="mb-3">
                    <label class="form-label fw-semibold">CGPA</label>
                    <input type="number" class="form-control" v-model="cgpa" step="any" />
                </div>

                <div class="d-flex gap-2">
                    <button type="submit" class="btn btn-primary w-100">Submit</button>
                    <RouterLink to="/student_dashboard" class="btn btn-secondary w-100">Go Back</RouterLink>
                </div>

            </form>
        </div>
    </div>
</template>

<style scoped>
</style>