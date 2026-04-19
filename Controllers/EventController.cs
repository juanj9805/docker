using Microsoft.AspNetCore.Mvc;
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
    
    [HttpGet]
    public IActionResult Create()
    {
        return View();
    }
    
    [HttpPost]
    public async Task<IActionResult> Create(CreateEventDto ev)
    {
        if (!ModelState.IsValid) return View(ev);
        var newEvent = new Event
        {
            Title = ev.Title,
            Img = ev.Img,
            Description = ev.Description,
            Location = ev.Location,
            Status = ev.Status,
        };
        
        await _context.AddAsync(newEvent);
        await _context.SaveChangesAsync();
        return RedirectToAction("Index");
    }
    [HttpGet]
    public async Task<IActionResult> Edit(int id)
    {
        var found =  await _context.Events.FirstOrDefaultAsync(ev => ev.Id == id);
        if (found == null) return NotFound();
        return View(found);
    } 
    
    [HttpPost]
    public async Task<IActionResult> Edit(EditEventDto ev, int id)
    {
        var found =  await _context.Events.FirstOrDefaultAsync(ev => ev.Id == id);

        if (found == null) return NotFound();

        if (!ModelState.IsValid) return View(ev);
        
        found.Title = ev.Title;
        found.Img = ev.Img;
        found.Description = ev.Description;
        found.Location = ev.Location;
        found.Status = ev.Status;
        
        await _context.SaveChangesAsync();
        return RedirectToAction("Index");
    } 
    
    [HttpPost]
    public async Task<IActionResult> Delete(int id)
    {
        var find = await _context.Events.FirstOrDefaultAsync(ev => ev.Id == id);
        if (find == null) return NotFound();
        _context.Events.Remove(find);
        await _context.SaveChangesAsync();
        return RedirectToAction("Index");
    } 
}