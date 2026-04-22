using Microsoft.AspNetCore.Mvc;
using vps.Data;
using vps.Models.Event;
using vps.Services;
using vps.Response;

namespace vps.Controllers;

public class EventController : Controller
{
    private readonly EventService _service;
    private readonly MysqlDbContext _context;
    public EventController(EventService service, MysqlDbContext context)
    {
        _context = context;
        _service = service;
    }
    
    [HttpGet]
    public async Task<IActionResult> Index(CancellationToken ct)
    {
        var events = _service.GetAll();
        return View();
    }
    
    [HttpGet]
    public IActionResult Create()
    {
        return View();
    }
    
    [HttpPost]
    public async Task<IActionResult> Create(CreateEventDto ev, CancellationToken ct)
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
        
        await _context.AddAsync(newEvent, ct);
        await _context.SaveChangesAsync(ct);
        return RedirectToAction("Index");
    }
    [HttpGet]
    public async Task<IActionResult> Edit(int id, CancellationToken ct)
    {
        var found =  await _context.Events.FirstOrDefaultAsync(ev => ev.Id == id, ct);
        if (found == null) return NotFound();
        var dto = new EditEventDto
        {
            Id = found.Id,
            Title = found.Title,
            Img = found.Img,
            Description = found.Description,
            Location = found.Location,
            Status = found.Status,
        };
        
        return View(dto);
    } 
    
    [HttpPost]
    public async Task<IActionResult> Edit(EditEventDto ev, int id, CancellationToken ct)
    {
        if (!ModelState.IsValid) return View(ev);
        var found =  await _context.Events.FirstOrDefaultAsync(ev => ev.Id == id, ct);
        if (found == null) return NotFound();
        
        found.Title = ev.Title;
        found.Img = ev.Img;
        found.Description = ev.Description;
        found.Location = ev.Location;
        found.Status = ev.Status;
        
        await _context.SaveChangesAsync(ct);
        return RedirectToAction("Index");
    } 
    
    [HttpPost]
    public async Task<IActionResult> Delete(int id, CancellationToken ct)
    {
        var find = await _context.Events.FirstOrDefaultAsync(ev => ev.Id == id, ct);
        if (find == null) return NotFound();
        _context.Events.Remove(find);
        await _context.SaveChangesAsync(ct);
        return RedirectToAction("Index");
    } 
}