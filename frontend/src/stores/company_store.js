import { ref } from "vue";
import { defineStore } from "pinia";
import { useAuthStore } from "./counter";

export const companyStore = defineStore('company_store', () => {
    const auth_store = useAuthStore()
    const pendingCompanies = ref([])
    const approvedCompanies = ref([])
    const error_value = ref('')

    async function fetchpendingCompanies(){
        try{
            const response = await fetch("http://127.0.0.1:5000/api/registered_companies",{
                method :"GET",
                headers:{
                    "Authentication-Token" : auth_store.getAuthToken()
                }
            })
            if(response.status === 401){
                pendingCompanies.value = []
                return 
            }
            if(response.ok){
                const output = await response.json()
                pendingCompanies.value = output
            }
        }
        catch(err){
            error_value.value = "You cannot view the admin page !!!"
        }
    }

    async function fetchapprovedCompanies(){
        try{
        const response = await fetch("http://127.0.0.1:5000/api/approved_companies",{
            method : 'GET',
            headers : {
                "Authentication-Token" : auth_store.getAuthToken()
            }

        })
        if(response.status === 401){
            approvedCompanies.value = []
            return 
        }
        if(response.ok){
            const output = await response.json()
            approvedCompanies.value = output
        }
    }
        catch(err){
            error_value.value = "You are not allowed to view admin functionality !!!"
        }
    }

    async function approve_company(CompanyId){
        try{
            const response = await fetch(`http://127.0.0.1:5000/api/approve_company/${CompanyId}`,{
            method:"PUT",
            headers:{
                "Authentication-Token" : auth_store.getAuthToken()
            }
        })
        if(response.ok){
            pendingCompanies.value = pendingCompanies.value.filter(p=>p.company_id !== CompanyId)
            await fetchapprovedCompanies()
            return true
        }
            }
    catch(err){
        error_value.value = "You are not allowed to view admin functionality !!!"
    }
    return false
}

    async function black_list(CompanyId){
        try{
        const response = await fetch(`http://127.0.0.1:5000/api/change_to_blacklist/${CompanyId}`,{
        method : "PUT",
        headers : {
            "Authentication-Token" : auth_store.getAuthToken()
        }
        })
        if(response.ok){
            approvedCompanies.value = approvedCompanies.value.filter(
                a => a.company_id !== CompanyId
            )
            return true
        }
    }
    catch(err){
        error_value.value = "You are not allowed to view admin functionality !!!"
    }
    return false
}
    return {pendingCompanies,approvedCompanies,error_value,fetchpendingCompanies,fetchapprovedCompanies,black_list,approve_company}
})
    