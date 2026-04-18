using Microsoft.AspNetCore.Mvc;
using vps.Data;

namespace vps.Controllers;

public class Event : Controller
{
    private readonly MysqlDbContext _context;
    public Event(MysqlDbContext context)
    {
        _context = context;
    }
    
    public IActionResult Index()
    {
        var events = _context.Events.ToList();
        return View(events);
    }
    
    public IActionResult Create()
    {
        return View();
    }
    public IActionResult Show()
    {
        return View();
    } 
    public IActionResult Edit()
    {
        return View();
    } 
    public IActionResult Destroy()
    {
        return View();
    } 
    // public IActionResult Update()
    // {
    //     return View();
    // } 
    // public IActionResult Store()
    // {
    //     return View();
    // } 
}