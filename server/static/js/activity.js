function getStats(authToken) {
    console.log(JSON.stringify(document.querySelector('[x-data]').__x.getUnobservedData()));
    return {
      isLoading: false,
      stats: null,
      fetchStats() {
        this.isLoading = true;
        fetch("/api/activity", { method: "GET", headers: { Authorization: `token ${authToken}` } })
          .then(resp => resp.json())
          .then(data => {
            this.isLoading = false;
            this.stats = data;
          });
      }
    }
}