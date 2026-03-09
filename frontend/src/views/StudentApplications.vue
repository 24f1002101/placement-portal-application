<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue';
import { useAuthStore } from '@/stores/counter';
import { useRoute} from 'vue-router';
const route = useRoute()
const auth_store = useAuthStore();
const user_email = auth_store.getUserEmail()
const auth_token = auth_store.getAuthToken()
const drive_id = route.params.drive_id
const applications = ref([])
async function fetch_applications(){
    const input = {
        drive_id : drive_id
    }
    const response = await fetch("http://127.0.0.1:5000/api/get_student_applications",{
        method : "POST",
        headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        },
        body : JSON.stringify(input)
    })
    if(response.ok){
        const output = await response.json()
        applications.value = output
    }
    else{
        alert(output.message)
        return
    }
}
onMounted(()=>{
    fetch_applications()
})
</script>

<template>
    <div>
        <div v-if="applications.length > 0 ">
            <table border="1">
                <thead>
                    <th>Name</th>
                    <th>Action</th>
                </thead>
                <tbody>
                    <tr v-for="application in applications">
                        <td>{{ application.student_name }}</td>
                        <td><RouterLink :to="`/review_application/${drive_id}/${application.student_id}`"><button>Review Application</button></RouterLink></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else>
            No Application Found !!!
        </div>
        <div>
            <RouterLink to="/company_dashboard"><button>Go Back</button></RouterLink>
        </div>
    </div>
</template>

<style scoped>
</style>