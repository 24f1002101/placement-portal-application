<script setup>
import { ref, onMounted, computed } from 'vue';
import { studentStore } from '@/stores/student_store';

const emit = defineEmits(['action-taken'])  // ADD THIS
const student_store = studentStore()
const props = defineProps({
    searchResults: Array,
    searchType: String
})
const approvedlist = computed(() => {
    if (props.searchType !== 'student') return []
    return props.searchResults.filter(s => s.status === 'approved')
})
const pendinglist = computed(() => {
    if (props.searchType !== 'student') return []
    return props.searchResults.filter(s => s.status === 'pending')
})

// UPDATED: emit after action
async function handleBlacklist(studentId) {
    const success = await student_store.black_list(studentId)
    if (success) emit('action-taken', studentId)
}

async function handleApprove(studentId) {
    const success = await student_store.approve_Student(studentId)
    if (success) emit('action-taken', studentId)
}

onMounted(async () => {
    await student_store.fetchpendingstudents()
    await student_store.Approvedstudents()
})
</script>

<template>
    <div>
        <div>
            <h2 v-if="!student_store.error_value">Registered Students</h2>

            <!-- IF SEARCHING -->
            <div v-if="searchType === 'student' && approvedlist.length">
                <div v-for="student in approvedlist" :key="student.id">
                    {{ student.name }}
                    <button @click="handleBlacklist(student.id)">Blacklist</button>  <!-- UPDATED -->
                </div>
            </div>

            <!-- ELSE NORMAL APPROVED LIST -->
            <div v-else>
                <div v-if="student_store.Approvedstudentslist.length === 0 && !student_store.error_value">
                    No Students Found !!!
                </div>
                <div v-for="student in student_store.Approvedstudentslist" :key="student.id">
                    {{ student.name }}
                    <button @click="student_store.black_list(student.id)">Blacklist</button>
                </div>
            </div>
        </div>

        <div>
            <h2 v-if="!student_store.error_value">To be approved Students</h2>

            <!-- IF SEARCHING -->
            <div v-if="searchType === 'student' && pendinglist.length">
                <div v-for="student in pendinglist" :key="student.id">
                    {{ student.name }}
                    <button @click="handleApprove(student.id)">Approve</button>  <!-- UPDATED -->
                </div>
            </div>

            <!-- ELSE NORMAL APPROVED LIST -->
            <div v-else>
                <div v-if="student_store.Pendingstudents.length === 0 && !student_store.error_value">
                    No Students Found !!!
                </div>
                <div v-for="student in student_store.Pendingstudents" :key="student.id">
                    {{ student.name }}
                    <button @click="student_store.approve_Student(student.id)">Approve</button>
                </div>
            </div>
        </div>
    </div>
</template>