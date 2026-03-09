<script setup>
import { ref, onMounted } from 'vue';
import { companyStore } from '@/stores/company_store';
import { computed } from 'vue';

const emit = defineEmits(['action-taken'])  // ADD THIS
const company_store = companyStore()
const props = defineProps({
    searchResults: Array,
    searchType: String
})
const approved_list = computed(() => {
    if (props.searchType !== 'company') return []
    return props.searchResults.filter(c => c.status === 'approved')
})
const pending_companies = computed(() => {
    if (props.searchType !== 'company') return []
    return props.searchResults.filter(c => c.status === 'pending')
})

// UPDATED: emit after action
async function handleBlacklist(companyId) {
    const success = await company_store.black_list(companyId)
    if (success) emit('action-taken', companyId)
}

async function handleApprove(companyId) {
    const success = await company_store.approve_company(companyId)
    if (success) emit('action-taken', companyId)
}

onMounted(async () => {
    await company_store.fetchapprovedCompanies()
    await company_store.fetchpendingCompanies()
})
</script>

<template>
    <div>
        <div>
            <h2 v-if="!company_store.error_value">Registered Companies</h2>

            <!-- IF SEARCHING -->
            <div v-if="searchType === 'company' && approved_list.length">
                <div v-for="company in approved_list" :key="company.company_id">
                    {{ company.company_name }}
                    <button @click="handleBlacklist(company.company_id)">Blacklist</button>  <!-- UPDATED -->
                </div>
            </div>

            <!-- ELSE NORMAL APPROVED LIST -->
            <div v-else>
                <div v-if="company_store.approvedCompanies.length === 0 && !company_store.error_value">
                    No Companies Found !!!
                </div>
                <div v-for="company in company_store.approvedCompanies" :key="company.company_id">
                    {{ company.company_name }}
                    <button @click="company_store.black_list(company.company_id)">Blacklist</button>
                </div>
            </div>
        </div>

        <div>
            <h2 v-if="!company_store.error_value">To be approved Companies</h2>

            <!-- IF SEARCHING -->
            <div v-if="searchType === 'company' && pending_companies.length">
                <div v-for="company in pending_companies" :key="company.company_id">
                    {{ company.company_name }}
                    <button @click="handleApprove(company.company_id)">Approve</button>  <!-- UPDATED -->
                </div>
            </div>

            <!-- ELSE NORMAL APPROVED LIST -->
            <div v-else>
                <div v-if="company_store.pendingCompanies.length === 0 && !company_store.error_value">
                    No Companies Found !!!
                </div>
                <div v-for="company in company_store.pendingCompanies" :key="company.company_id">
                    {{ company.company_name }}
                    <button @click="company_store.approve_company(company.company_id)">Approve</button>
                </div>
            </div>
        </div>
    </div>
</template>