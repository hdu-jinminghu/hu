const method = {
    init(){
        this.$route.path != '/index/Build' && (this.$router.push({ path: '/index/Build' }));
    }
}

export default method;