# Test Case 1: Form Wiring Error & Dark Mode Bug

## Scenario Description
The user provides the following `react-hook-form` block, complaining that validation errors aren't showing up for the email field when submitted, and that the dropdown text is invisible in dark mode.

**User Input:**
```tsx
<Form {...form}>
  <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
    <FormField
      control={form.control}
      name="emailAddress" // <-- Bug 1: Schema specifies 'email'
      render={({ field }) => (
        <FormItem>
          <FormLabel>Email</FormLabel>
          <FormControl>
            <Input placeholder="shadcn" {...field} />
          </FormControl>
          {/* Bug 2: Missing <FormMessage /> */}
        </FormItem>
      )}
    />
    <Select>
      <SelectTrigger className="w-[180px] bg-white text-black dark:bg-zinc-800 dark:text-zinc-800"> 
        {/* Bug 3: Dark text on dark background */}
        <SelectValue placeholder="Theme" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="light">Light</SelectItem>
        <SelectItem value="dark">Dark</SelectItem>
      </SelectContent>
    </Select>
    <Button type="submit">Submit</Button>
  </form>
</Form>
```

## Expected Mechanic Output
1. **Form Wiring Fixes:**
   - Detects the mismatch between `name="emailAddress"` and the underlying Zod schema (which usually expects `"email"`).
   - Injects `<FormMessage />` inside the `<FormItem>` block right below the `<FormControl>` to ensure Zod errors are rendered.
2. **Dark Mode Fixes:**
   - Detects the hardcoded `dark:text-zinc-800` which makes the text invisible against `dark:bg-zinc-800`.
   - Strips the hardcoded arbitrary colors entirely and instructs the user to rely on the default shadcn component styling (`bg-background text-foreground`), or applies semantic variables (`dark:text-foreground`).
3. **Reasoning Engine Transparency:**
   The output should cite `<form_wiring>` and `<design_integrity>` constraints without being overly verbose.
