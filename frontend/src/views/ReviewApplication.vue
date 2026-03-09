<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/counter';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import router from '@/router';

const auth_store = useAuthStore();
const route = useRoute();
const drive_id = route.params.drive_id
const student_id = route.params.student_id
const auth_token = auth_store.getAuthToken()
const student_name = ref('')
const branch = ref('')
const year = ref(1)
const cgpa = ref(3.67)
const job_role = ref('')
const seleced_value = ref('')

async function fetch_application_details(){
    const input = {
        drive_id : drive_id,
        student_id : student_id
    }
    const response = await fetch("http://127.0.0.1:5000/api/get_student_application_details",{
        method : "POST",
        headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        },
        body : JSON.stringify(input)
    })
    if(response.ok){
        const output = await response.json()
        student_name.value = output.student_name
        branch.value = output.branch
        year.value = output.year
        cgpa.value = output.cgpa
        job_role.value = output.job_role
    } else {
        const output = await response.json()
        alert(output.message)
        return
    }
}

async function change_details(student_id, drive_id){
    const auth_token = auth_store.getAuthToken()
    const input = {
        student_id : student_id,
        drive_id : drive_id,
        value : seleced_value.value
    }
    const response = await fetch("http://127.0.0.1:5000/api/change_details_application",{
        method : "PUT",
        headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        },
        body : JSON.stringify(input)
    })
    if(response.ok){
        const output = await response.json()
        alert(output.message)
        router.push(`/get_applications/${drive_id}`)
    } else {
        const output = await response.json()
        alert(output.message)
    }
}

async function view_resume(student_id, drive_id){
    const input = {
        student_id : student_id,
        drive_id : drive_id
    }
    const response = await fetch("http://127.0.0.1:5000/api/view_resume",{
        method : "POST",
        headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        },
        body : JSON.stringify(input)
    })
    if(response.ok){
        const blob = await response.blob()
        const url = URL.createObjectURL(blob)
        window.open(url, '_blank')
    } else {
        const output = await response.json()
        alert(output.message)
    }
}

onMounted(()=>{
    fetch_application_details()
})
</script>

<template>
    <div class="container mt-5">
        <div class="card p-4 shadow-sm" style="max-width: 500px; margin: auto;">
            <h5 class="fw-bold mb-4">Application Details</h5>

            <table class="table table-bordered mb-4">
                <tbody>
                    <tr>
                        <th>Student Name</th>
                        <td>{{ student_name }}</td>
                    </tr>
                    <tr>
                        <th>Branch</th>
                        <td>{{ branch }}</td>
                    </tr>
                    <tr>
                        <th>Year</th>
                        <td>{{ year }}</td>
                    </tr>
                    <tr>
                        <th>CGPA</th>
                        <td>{{ cgpa }}</td>
                    </tr>
                    <tr>
                        <th>Job Role</th>
                        <td>{{ job_role }}</td>
                    </tr>
                </tbody>
            </table>

            <button class="btn btn-primary w-100 mb-3" @click="view_resume(student_id, drive_id)">
                View Resume
            </button>

            <div class="mb-3">
                <label class="form-label fw-semibold">Update Status</label>
                <select class="form-select" v-model="seleced_value">
                    <option value="shortlisted">Shortlisted</option>
                    <option value="waiting">Waiting</option>
                    <option value="rejected">Reject</option>
                </select>
            </div>

            <button class="btn btn-success w-100" @click="change_details(student_id, drive_id)">
                Save
            </button>
        </div>
    </div>
</template>

<style scoped>
</style>