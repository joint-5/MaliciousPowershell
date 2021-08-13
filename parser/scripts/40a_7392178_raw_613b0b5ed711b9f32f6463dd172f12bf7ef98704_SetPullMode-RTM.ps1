Configuration SetPullMode
{
    Node Server01
    {
         # Set the DSC engine (LCM) to Pull mode
          LocalConfigurationManager
          {
              ConfigurationID           = "e528dee8-6f0b-4885-98a1-1ee4d8e86d82"
              ConfigurationMode         = "ApplyOnly"
              RefreshMode               = "Pull"
              DownloadManagerName       = "WebDownloadManager"
              DownloadManagerCustomData = @{
                  ServerUrl = "http://<PullServer>:8080/PSDSCPullServer/PSDSCPullServer.svc" ;
                  AllowUnsecureConnection = "true";
              }
          }
    }
}
SetPullMode
Set-DSCLocalConfigurationManager -ComputerName Server01 -Path .\SetPullMode -Verbose 
