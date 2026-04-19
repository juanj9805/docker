using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;
using vps.Models;
using Microsoft.EntityFrameworkCore;
using vps.Data;
using vps.Models.Event;

namespace vps.Controllers;

public class EventController : Controller
{
    private readonly MysqlDbContext _context;
    public EventController(MysqlDbContext context)
    {
        _context = context;
    }
    
    [HttpGet]
    public async Task<IActionResult> Index()
    {
        var events = await _context.Events.ToListAsync();
        return View(events);
    }
    
    public IActionResult Details()
    {
        return View();
    }
        
    [HttpGet]
    public IActionResult Create()
    {
        
        return View();
    }
    
    [HttpPost]
    public async Task<IActionResult> Create(Event ev)
    {
        _context.AddAsync(ev);
        await _context.SaveChangesAsync();
        return RedirectToAction("Index");
    }
    [HttpGet]
    public IActionResult Edit(int Id)
    {
        return View();
    } 
    [HttpPost]
    public async Task<IActionResult> Edit(Event ev)
    {
        
        return View();
    } 
    [HttpPost]
    public async Task<IActionResult> Delete()
    {
        return View();
    } 
}