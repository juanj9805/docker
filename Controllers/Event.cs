using Microsoft.AspNetCore.Mvc;

namespace vps.Controllers;

public class Event : Controller
{
    public IActionResult Index()
    {
        return View();
    }
    
    public IActionResult Show()
    {
        return View();
    } 
}