using System.Net.Http.Headers;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace CCS.Pages;

public class IndexModel : PageModel
{
    private readonly ILogger<IndexModel> _logger;

    public string Environment { get; set; }

    public string Weather { get; set; }

    public string BgColor{ get; set; }

    public IndexModel(ILogger<IndexModel> logger)
    {
        _logger = logger;
    }

    public void OnGet()
    {
        Environment = System.Environment.GetEnvironmentVariable("environment");
        BgColor = System.Environment.GetEnvironmentVariable("bgcolor");
        
        if (null == Environment)
            Environment = "NOT PROVIDED";

        if (null == BgColor)
            BgColor = "FFFF00";
            
        Weather = QueryAPI();
    }

    private string QueryAPI()
    {
        string ret = "";

        try
        {

            HttpClient client = new() { BaseAddress = new Uri("https://api.open-meteo.com") };

            client.DefaultRequestHeaders.Accept.Clear();
            client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
            
            Random rnd = new();

            string path = "/v1/forecast?latitude=49.1011&longitude=-122.6588&current=temperature_2m&daily=temperature_2m_max,temperature_2m_min&forecast_days=1";

            try
            {
                HttpResponseMessage response = client.GetAsync(path).Result;
                
                if (response.IsSuccessStatusCode)
                {
                    ret = response.Content.ReadAsStringAsync().Result;
                }
                else
                {
                    ret = "Calling the service got " + response.StatusCode + "\r\n" + response.Content;
                }
            }
            catch (Exception ex)
            {
                ret = "Erro calling " + client.BaseAddress + "\r\n" + ex.ToString();
            }
        }
        catch
        {
            ret = "Error calling Weather API";
        }

        return ret;
    }    
}
