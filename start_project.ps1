# Start Big Data Project Script

Write-Host "Starting Big Data Project..." -ForegroundColor Cyan

# 1. Check if Docker is running
Write-Host "Checking Docker status..."
docker info > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Docker is not running. Please start Docker Desktop and try again." -ForegroundColor Red
    exit 1
}

# 2. Build and Start Containers
Write-Host "Building and starting Docker containers..." -ForegroundColor Yellow
docker-compose up -d --build

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to start containers via docker-compose." -ForegroundColor Red
    exit 1
}

# 3. Wait for services to be ready
Write-Host "Waiting 30 seconds for services to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# 4. Open UIs in default browser
Write-Host "Opening User Interfaces..." -ForegroundColor Green

# Hadoop NameNode (HDFS)
Start-Process "http://localhost:19870"

# Kafka UI
Start-Process "http://localhost:18080"

# Streamlit Dashboard
Start-Process "http://localhost:18501"

Write-Host "---------------------------------------------------"
Write-Host "Project started successfully!" -ForegroundColor Green
Write-Host "HDFS:      http://localhost:19870"
Write-Host "Kafka UI:  http://localhost:18080"
Write-Host "Dashboard: http://localhost:18501"
Write-Host "---------------------------------------------------"
