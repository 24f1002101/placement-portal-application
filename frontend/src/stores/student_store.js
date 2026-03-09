import { ref } from "vue"
import { defineStore } from "pinia"
import { useAuthStore } from "./counter"
export const studentStore = defineStore('student_store', () => {
    const auth_store = useAuthStore()
    const Pendingstudents = ref([])
    const Approvedstudentslist = ref([])
    let error_value = ref('')
    async function fetchpendingstudents(){
    try{
    const response = await fetch("http://127.0.0.1:5000/api/registered_students",{
      method : "GET",
      headers : {
        "Authentication-Token" : auth_store.getAuthToken()
      }
    })
    if(response.status === 405){
        error_value = "Unauthorized"
        Pendingstudents.value = []
        return 
    }
    if(response.ok){
        Pendingstudents.value = await response.json()
    }
    }
    catch(err){
        error_value.value = "You are not allowed to view admin functionalities !!!"
  }
}

  async function Approvedstudents() {
    try{
        const response = await fetch("http://127.0.0.1:5000/api/approved_students",{
            method : "GET",
            headers : {
                "Authentication-Token" : auth_store.getAuthToken()
            }
        })
        if(response.status === 401){
            Approvedstudentslist.value = []
            return 
        }
        if(response.ok){
            const output = await response.json()
            Approvedstudentslist.value = output
        }
    }
    catch(err){
        error_value.value = "You are not allowed to view the admin functionalities !!!"
    }
  }

async function black_list(StudentId){
    try{
    const response = await fetch(`http://127.0.0.1:5000/api/change_to_blacklist_student/${StudentId}`,{
        method:"PUT",
        headers :{
            "Authentication-Token" : auth_store.getAuthToken()
        }
    })
    if(response.ok){
            Approvedstudentslist.value =
                Approvedstudentslist.value.filter(
                    s => s.id !== StudentId
                )
                return true
        }
        
    }
    catch(err){
         error_value.value = "You are not allowed to view the admin functionalities !!!"
    }
    return false
}

async function approve_Student(studentId){
    try{
    const response = await fetch(`http://127.0.0.1:5000/api/approve_student/${studentId}`,{
        method : "PUT",
        headers : {
            "Authentication-Token" : auth_store.getAuthToken()
        }
    })
    if(response.ok){
        const output = await response.json()
        Pendingstudents.value = Pendingstudents.value.filter(s=>s.id!==studentId)
        await Approvedstudents()
        return true;
    }
    
}
catch(err){
    error_value.value = "You are not allowed to view admin functionalities !!!"
}
return false;
}
  return {Approvedstudentslist,Pendingstudents,approve_Student,black_list,Approvedstudents,fetchpendingstudents,error_value}
})